import { Injectable, Inject, HttpException, HttpStatus } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { lastValueFrom } from 'rxjs';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { eq, and, desc, lt } from 'drizzle-orm';
import { ConfigService } from '@nestjs/config';
import { Cron, CronExpression } from '@nestjs/schedule';

import { orders } from '../database/schema';
import { CreateOrderDto } from './dto/create-order.dto';
import * as schema from '../database/schema';

@Injectable()
export class OrdersService {
  private readonly inventoryServiceUrl: string;

  constructor(
    @Inject('DB_CONNECTION') private readonly db: NodePgDatabase<typeof schema>,
    private readonly httpService: HttpService,
    private readonly configService: ConfigService,
  ) {
    const inventoryServiceUrl = this.configService.get<string>(
      'INVENTORY_SERVICE_URL',
    );

    if (!inventoryServiceUrl) {
      throw new Error(
        ` SYSTEM HALTED: please add INVENTORY_SERVICE_URL in .env`,
      );
    }

    this.inventoryServiceUrl = inventoryServiceUrl;
  }

  async createOrder(
    createOrderDto: CreateOrderDto,
    userId: string,
    authHeader: string,
  ) {
    try {
      const ticketResponse = await lastValueFrom(
        this.httpService.get(
          `${this.inventoryServiceUrl}/events/${createOrderDto.event_id}/ticket_type_id/${createOrderDto.ticket_type_id}`,
          {
            headers: { Authorization: authHeader },
          },
        ),
      );

      const ticket = ticketResponse.data;
      const totalAmount = (
        parseFloat(ticket.price) * createOrderDto.quantity
      ).toFixed(2);

      const newOrder = await this.db
        .insert(orders)
        .values({
          userId: userId,
          reservationId: createOrderDto.reservation_id,
          eventId: createOrderDto.event_id,
          ticketTypeId: createOrderDto.ticket_type_id,
          ticketQuantity: createOrderDto.quantity,
          totalAmount: totalAmount,
          status: 'PENDING',
        })
        .returning();

      return newOrder;
    } catch (error: any) {
      throw new HttpException(
        error.response?.data?.detail ||
          'Failed to create order. Could not communicate with inventory Service.',
        error.response?.status || HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getOrderById(orderId: string, userId: string) {
    const result = await this.db
      .select()
      .from(orders)
      .where(and(eq(orders.id, orderId), eq(orders.userId, userId)));

    if (result.length === 0) {
      throw new HttpException('Order not found', HttpStatus.NOT_FOUND);
    }
    return result;
  }

  async getUserOrders(userId: string) {
    return await this.db
      .select()
      .from(orders)
      .where(eq(orders.userId, userId))
      .orderBy(desc(orders.createdAt));
  }

  async cancelOrder(orderId: string, userId: string, authHeader: string) {
    const orderArr = await this.getOrderById(orderId, userId);
    const order = orderArr[0];

    if (order.status !== 'PENDING') {
      throw new HttpException(
        'Only Pending orders can be cancelled.',
        HttpStatus.BAD_GATEWAY,
      );
    }

    const updatedOrder = await this.db
      .update(orders)
      .set({ status: 'CANCELLED', updatedAt: new Date() })
      .where(eq(orders.id, orderId))
      .returning();

    try {
      await lastValueFrom(
        this.httpService.delete(
          `${this.inventoryServiceUrl}/reservations/${order.reservationId}`,
          {
            headers: { Authorization: authHeader },
          },
        ),
      );
    } catch (error) {
      console.error('Failed to release tickets in Inventory Service: ', error);
    }

    return updatedOrder;
  }

  async updateOrderStatus(
    orderId: string,
    status: 'COMPLETED' | 'CANCELLED' | 'REFUNDED',
  ) {
    const updatedOrder = await this.db
      .update(orders)
      .set({ status, updatedAt: new Date() })
      .returning();

    if (updatedOrder.length === 0) {
      throw new HttpException('Order not found', HttpStatus.NOT_FOUND);
    }

    // Note: If status === 'COMPLETED', we will later need to tell the
    // Inventory Service to mark the reservation as 'CONVERTED'.

    return updatedOrder;
  }

  @Cron(CronExpression.EVERY_5_MINUTES)
  async cleanUpStaleOrders() {
    console.log('Running stale orders cleanup...');

    // Update any PENDING order older than 15 minutes to CANCELLED
    const fifteenMinutesAgo = new Date(Date.now() - 15 * 60 * 1000);

    await this.db
      .update(orders)
      .set({ status: 'CANCELLED', updatedAt: new Date() })
      .where(
        and(
          eq(orders.status, 'PENDING'),
          lt(orders.createdAt, fifteenMinutesAgo),
        ),
      );
  }
}

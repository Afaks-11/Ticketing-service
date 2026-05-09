import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ConfigService } from '@nestjs/config';
import { lastValueFrom } from 'rxjs';

@Injectable()
export class OrderService {
  private readonly orderServiceUrl: string;
  constructor(
    private readonly httpService: HttpService,
    private readonly configService: ConfigService,
  ) {
    const orderServiceUrl = this.configService.get<string>('ORDER_SERVICE_URL');

    if (!orderServiceUrl) {
      throw new Error(' SYSTEM HALTED: please add ORDER_SERVICE_URL in .nev');
    }

    this.orderServiceUrl = orderServiceUrl;
  }

  async createOrder(createOrderDto: any, userId, authHeader: string) {
    try {
      const response = await lastValueFrom(
        this.httpService.post(
          `${this.orderServiceUrl}/orders`,
          createOrderDto,
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );

      return response.data;
    } catch (error: any) {
      throw new HttpException(
        error.response?.data?.message || 'Order Service Error',
        error.response?.status || HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getorderById(orderId: string, userId: string, authHeader: string) {
    try {
      const response = await lastValueFrom(
        this.httpService.get(`${this.orderServiceUrl}/orders/${orderId}`, {
          headers: {
            Authorization: authHeader,
          },
        }),
      );

      return response.data;
    } catch (error: any) {
      throw new HttpException(
        error.response?.data?.message || 'Order Service Error',
        error.response?.status || HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getUserOrders(userId: string, authHeader: string) {
    try {
      const response = await lastValueFrom(
        this.httpService.get(`${this.orderServiceUrl}/orders/my-orders`, {
          headers: {
            Authorization: authHeader,
          },
        }),
      );

      return response.data;
    } catch (error: any) {
      throw new HttpException(
        error.response?.data?.message || 'Order Service Error',
        error.response?.status || HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async cancelOrder(orderId: string, userId: string, authHeader: string) {
    try {
      const response = await lastValueFrom(
        this.httpService.post(
          `${this.orderServiceUrl}/orders/${orderId}/cancel`,
          {},
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );

      return response.data;
    } catch (error: any) {
      throw new HttpException(
        error.response?.data?.message || 'Order Service Error',
        error.response?.status || HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}

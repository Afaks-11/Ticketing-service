import {
  Controller,
  Post,
  Patch,
  Get,
  Param,
  Body,
  Req,
  Headers,
  UseGuards,
  ParseUUIDPipe,
} from '@nestjs/common';
import { OrdersService } from './orders.service';
import { CreateOrderDto } from './dto/create-order.dto';
import { JwtAuthGuard } from 'src/auth/jwt-auth.guard';

@Controller('orders')
export class OrdersController {
  constructor(private readonly ordersService: OrdersService) {}

  @Post()
  async createOrder(
    @Body() createOrderDto: CreateOrderDto,
    @Req() req: any,
    @Headers('Authorization') authHeader: string,
  ) {
    const userId = req.user.sub || req.user.id;

    return this.ordersService.createOrder(createOrderDto, userId, authHeader);
  }

  @Get('my-orders')
  async getUserOrders(@Req() req: any) {
    const userId = req.user.sub || req.user.id;
    return this.ordersService.getUserOrders(userId);
  }

  @Get(':id')
  async getOrderById(
    @Param('id', ParseUUIDPipe) orderId: string,
    @Req() req: any,
  ) {
    const userId = req.user.sub || req.user.id;
    return this.ordersService.getOrderById(orderId, userId);
  }

  @Post(':id/cancel')
  async cancelOrder(
    @Param('id', ParseUUIDPipe) orderId: string,
    @Req() req: any,
    @Headers('authorization') authHeader: string,
  ) {
    const userId = req.user.sub || req.user.id;
    return this.ordersService.cancelOrder(orderId, userId, authHeader);
  }

  @Post(':id/status')
  async updateStatus(
    @Param('id', ParseUUIDPipe) orderId: string,
    @Body('status') status: 'COMPLETED' | 'CANCELLED' | 'REFUNDED',
  ) {
    return this.ordersService.updateOrderStatus(orderId, status);
  }
}

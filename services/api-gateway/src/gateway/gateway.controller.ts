import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { GatewayService } from './gateway.service';

@Controller('api')
export class GatewayController {
  constructor(private readonly gatewayService: GatewayService) {}

  @Get('inventory')
  async getInventory() {
    return this.gatewayService.forwardRequest(
      'http://localhost:8001/items',
      'GET',
    );
  }

  @Post('orders')
  async createOrder(@Body() body: any) {
    const transformedPayload = {
      product_id: body.productId,
      quantity: body.qty,
    };

    return this.gatewayService.forwardRequest(
      'http://localhost:8002/create-order',
      'POST',
      transformedPayload,
    );
  }

  @Post('payments')
  async makePayment(@Body() body: any) {
    return this.gatewayService.forwardRequest(
      'http://localhost:8003/pay',
      'POST',
      body,
    );
  }
}

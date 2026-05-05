import {
  Controller,
  Body,
  Post,
  Get,
  Patch,
  Delete,
  Param,
  Req,
  UseGuards,
  ParseUUIDPipe,
} from '@nestjs/common';
import { ReservationsService } from './reservations.service';
import { JwtAuthGuard } from 'src/common/auth.guard';

@Controller('reservations')
@UseGuards(JwtAuthGuard)
export class ReservationsController {
  constructor(private readonly reservationService: ReservationsService) {}

  @Post()
  async createReservation(@Body() body: any, @Req() req: any) {
    const userId = req.user.sub || req.user.id;

    const payloadForFastAPI = {
      ...body,
      user_id: userId,
    };

    return this.reservationService.createReservation(payloadForFastAPI);
  }

  @Get(':reservation_id')
  async getReservation(
    @Param('reservation_id', ParseUUIDPipe) reservationId: string,
  ) {
    return this.reservationService.getReservation(reservationId);
  }

  @Patch(':reservation_id')
  async extendReservation(
    @Param('reservation_id', ParseUUIDPipe) reservationId: string,
    @Body() updatePayload: any,
  ) {
    return this.reservationService.extendReservation(
      reservationId,
      updatePayload,
    );
  }

  @Delete(':reservation_id')
  async deleteReservation(
    @Param('reservation_id', ParseUUIDPipe) reservationId: string,
  ) {
    return this.reservationService.deleteReservation(reservationId);
  }
}

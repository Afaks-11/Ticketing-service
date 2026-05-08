import {
  Controller,
  UseGuards,
  Post,
  Get,
  Patch,
  Delete,
  Param,
  Body,
  Req,
  Headers,
  ParseUUIDPipe,
} from '@nestjs/common';
import { JwtAuthGuard } from 'src/common/auth.guard';
import { TicketsService } from './tickets.service';

@UseGuards(JwtAuthGuard)
@Controller('events')
export class TicketsController {
  constructor(private readonly ticketService: TicketsService) {}

  @Post(':event_id/ticket-types')
  async createTicket(
    @Param('event_id', ParseUUIDPipe) eventId: string,
    @Body() body: any,
    @Headers('authorization') authHeader: string,
  ) {
    const payload = {
      ...body,
    };

    return this.ticketService.createTicket(payload, eventId, authHeader);
  }

  @Get(':event_id/ticket-types')
  async getEventTicketTypes(
    @Param('event_id', ParseUUIDPipe) eventId: string,
    @Headers('authorization') authHeader: string,
  ) {
    return this.ticketService.getEventTicketTypes(eventId, authHeader);
  }

  @Get(':event_id/ticket-types/:ticket_id')
  async getEventTicketTypeById(
    @Param('event_id', ParseUUIDPipe)
    eventId: string,
    @Param('ticket_id', ParseUUIDPipe)
    ticketId: string,
    @Headers('authorization') authHeader: string,
  ) {
    return this.ticketService.getEventTicketTypeById(
      eventId,
      ticketId,
      authHeader,
    );
  }

  @Patch(':event_id/ticket-types/:ticket_id')
  async updateEventTicketTypeById(
    @Param('event_id', ParseUUIDPipe)
    eventId: string,
    @Param('ticket_id', ParseUUIDPipe)
    ticketId: string,
    @Headers('authorization') authHeader: string,
    @Body() updatePayload: any,
  ) {
    return this.ticketService.updateEventTicketTypeById(
      eventId,
      ticketId,
      updatePayload,
      authHeader,
    );
  }

  @Delete(':event_id/ticket-types/:ticket_id')
  async deleteEventTicketTypeById(
    @Param('event_id', ParseUUIDPipe)
    eventId: string,
    @Param('ticket_id', ParseUUIDPipe)
    ticketId: string,
    @Headers('authorization') authHeader: string,
  ) {
    return this.ticketService.deleteEventTicketTypeById(
      eventId,
      ticketId,
      authHeader,
    );
  }
}

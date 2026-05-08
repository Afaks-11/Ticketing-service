import {
  Controller,
  Get,
  Post,
  Body,
  UseGuards,
  Headers,
  Param,
  ParseUUIDPipe,
  Delete,
} from '@nestjs/common';
import { EventsService } from './events.service';
import { JwtAuthGuard } from 'src/common/auth.guard';

@UseGuards(JwtAuthGuard)
@Controller('events')
export class EventsController {
  constructor(private readonly eventService: EventsService) {}

  @Post()
  async createEvent(
    @Body() payloadCreate: any,
    @Headers('authorization') authHeader: string,
  ) {
    return this.eventService.createEvent(payloadCreate, authHeader);
  }

  @Get()
  async getEvent(@Headers('authorization') authHeader: string) {
    return this.eventService.getEvent(authHeader);
  }

  @Get(':event_id')
  async getEventById(
    @Headers('authorization') authHeader: string,
    @Param('event_id', ParseUUIDPipe) eventId: string,
  ) {
    return this.eventService.getEventById(authHeader, eventId);
  }

  @Delete(':event_id')
  async deleteEventById(
    @Headers('authorization') authHeader: string,
    @Param('event_id', ParseUUIDPipe) eventId: string,
  ) {
    return this.eventService.deleteEventById(authHeader, eventId);
  }
}

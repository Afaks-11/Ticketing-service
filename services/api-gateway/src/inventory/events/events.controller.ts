import { Controller, Get, Post, Body } from '@nestjs/common';
import { EventsService } from './events.service';

@Controller('events')
export class EventsController {
  constructor(private readonly eventService: EventsService) {}

  @Post()
  async createEvent(@Body() payloadCreate: any) {
    return this.eventService.createEvent(payloadCreate);
  }

  @Get()
  async getEvent() {
    return this.eventService.getEvent();
  }
}

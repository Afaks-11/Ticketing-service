import { Controller, Get, Post, Body, UseGuards } from '@nestjs/common';
import { EventsService } from './events.service';
import { JwtAuthGuard } from 'src/common/auth.guard';

@Controller('events')
@UseGuards(JwtAuthGuard)
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

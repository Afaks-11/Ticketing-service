import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { TicketsService } from './tickets.service';
import { TicketsController } from './tickets.controller';

@Module({
  imports: [HttpModule],
  controllers: [TicketsController],
  providers: [TicketsService],
})
export class TicketsModule {}

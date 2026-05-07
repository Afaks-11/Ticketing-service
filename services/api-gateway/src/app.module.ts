import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AuthModule } from './auth/auth.module';
import { JwtModule } from '@nestjs/jwt';
import { ReservationsModule } from './inventory/reservations/reservations.module';
import { TicketsModule } from './inventory/tickets/tickets.module';
import { EventsModule } from './inventory/events/events.module';


@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),
    JwtModule.register({ global: true }),
    AuthModule,
    EventsModule,
    TicketsModule,
    ReservationsModule,
  ],
})
export class AppModule {}

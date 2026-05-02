import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { PrismaModule } from 'src/prisma/prisma.module';

@Module({
  imports: [
    PrismaModule,
    JwtModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: async (configService: ConfigService) => {
        const secret = configService.get<string>('JWT_SECRET');
        const expiration = configService.get<string>('JWT_EXPIRATION');

        if (!secret) {
          throw new Error(
            ' SYSTEM HALTED: Missing JWT_SECRET. Please add it to your .env file.',
          );
        }

        if (!expiration) {
          throw new Error(
            ' SYSTEM HALTED: Missing JWT_EXPIRATION. Please add it to your .env file (e.g., JWT_EXPIRATION=3600).',
          );
        }

        return {
          secret: secret,
          signOptions: { expiresIn: parseInt(expiration, 10) },
        };
      },
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService],
})
export class AuthModule {}

import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { Logger } from '@nestjs/common';

async function bootstrap() {
  const logger = new Logger('bootstrap')
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3003);
  logger.log('Order servvice running on port 3003')
}
bootstrap();

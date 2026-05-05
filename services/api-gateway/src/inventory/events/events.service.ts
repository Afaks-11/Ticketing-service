import { Injectable, HttpException } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { lastValueFrom } from 'rxjs';

@Injectable()
export class EventsService {
  private readonly INVENTORY_URL = 'http://localhost:3002';

  constructor(private readonly httpService: HttpService) {}

  async createEvent(payloadCreate) {
    try {
      const response = await lastValueFrom(
        this.httpService.post(`${this.INVENTORY_URL}/events`, payloadCreate),
      );

      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new HttpException(
          error.response.data.detail || 'Failed to create Event',
          error.response.status,
        );
      }
      throw new HttpException('Could not connect to Inventory Service', 500);
    }
  }

  async getEvent() {
    try {
      const response = await lastValueFrom(
        this.httpService.get(`${this.INVENTORY_URL}/events`),
      );

      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new HttpException(
          error.response.data.detail || 'Failed to get Events',
          error.response.status,
        );
      }
      throw new HttpException('Could not connect to Inventory Service', 500);
    }
  }
}

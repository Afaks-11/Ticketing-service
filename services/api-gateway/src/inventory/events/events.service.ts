import { Injectable, HttpException } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { lastValueFrom } from 'rxjs';

@Injectable()
export class EventsService {
  private readonly INVENTORY_URL = 'http://localhost:3002';

  constructor(private readonly httpService: HttpService) {}

  async createEvent(payloadCreate, authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.post(`${this.INVENTORY_URL}/events`, payloadCreate, {
          headers: {
            Authorization: authHeader,
          },
        }),
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

  async getEvent(authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.get(`${this.INVENTORY_URL}/events`, {
          headers: {
            Authorization: authHeader,
          },
        }),
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

  async getEventById(authHeader, eventId) {
    try {
      const response = await lastValueFrom(
        this.httpService.get(`${this.INVENTORY_URL}/events/${eventId}`, {
          headers: {
            Authorization: authHeader,
          },
        }),
      );

      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new HttpException(
          error.response.data.detail ||
            'Could not connect to Inventory Service',
          error.response.status || 500,
        );
      }
    }
  }

  async deleteEventById(authHeader, eventId) {
    try {
      const response = await lastValueFrom(
        this.httpService.delete(`${this.INVENTORY_URL}/events/${eventId}`, {
          headers: {
            Authorization: authHeader,
          },
        }),
      );

      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new HttpException(
          error.response.data.detail ||
            'Could not connect to Inventory Service',
          error.response.status || 500,
        );
      }
    }
  }
}

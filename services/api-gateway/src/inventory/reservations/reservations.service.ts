import { Injectable, HttpException } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { lastValueFrom } from 'rxjs';

@Injectable()
export class ReservationsService {
  private readonly INVENTORY_URL = 'http://localhost:3002';

  constructor(private readonly httpService: HttpService) {}

  async createReservation(payload: any, authHeader: string) {
    try {
      const response = await lastValueFrom(
        this.httpService.post(`${this.INVENTORY_URL}/reservations`, payload, {
          headers: {
            Authorization: authHeader,
          },
        }),
      );

      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new HttpException(
          error.response.data.detail || 'Inventory Service Error',
          error.response.status,
        );
      }

      throw new HttpException('Could not connect to Inventory Service', 500);
    }
  }

  async getReservation(reservation_id: string, authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.get(
          `${this.INVENTORY_URL}/reservations/${reservation_id}`,
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );

      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new HttpException(
          error.response.data.detail || 'Failed to get Reservation',
          error.response.status,
        );
      }
      throw new HttpException('Could not connect to Inventory Service', 500);
    }
  }

  async extendReservation(reservation_id: string, payload: any, authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.patch(
          `${this.INVENTORY_URL}/reservations/${reservation_id}`,
          payload,
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );

      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new HttpException(
          error.response.data.detail || 'Failed to update reservation',
          error.response.status,
        );
      }

      throw new HttpException('Could not connect to Inventory Service', 500);
    }
  }

  async deleteReservation(reservation_id: string, authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.delete(
          `${this.INVENTORY_URL}/reservations/${reservation_id}`,
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );
    } catch (error: any) {
      if (error.response) {
        (error.response.data.detail || 'Failed to delete Reservation',
          error.response.status);
      }
      throw new HttpException('Could not connect to Inventory Service', 500);
    }
  }
}

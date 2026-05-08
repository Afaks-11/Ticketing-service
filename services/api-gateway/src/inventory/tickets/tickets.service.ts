import { Injectable, HttpException } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { lastValueFrom } from 'rxjs';

@Injectable()
export class TicketsService {
  private readonly INVENTORY_URL = 'http://localhost:3002';

  constructor(private readonly httpService: HttpService) {}

  async createTicket(payload, eventId, authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.post(
          `${this.INVENTORY_URL}/events/${eventId}/ticket-types`,
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
      throw new HttpException(
        error.response.data.detail || 'Could not connect to Inventory Service',
        error.response.status || 500,
      );
    }
  }

  async getEventTicketTypes(eventId, authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.get(
          `${this.INVENTORY_URL}/events/${eventId}/ticket-types`,
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );

      return response.data;
    } catch (error: any) {
      throw new HttpException(
        error.response.data.detail || 'Could not connect to Inventory Service',
        error.response.status || 500,
      );
    }
  }

  async getEventTicketTypeById(eventId, ticketId, authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.get(
          `${this.INVENTORY_URL}/events/${eventId}/ticket-types/${ticketId}`,
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );

      return response.data;
    } catch (error: any) {
      throw new HttpException(
        error.response.data.detail || 'Could not connect to Inventory Service',
        error.response.status || 500,
      );
    }
  }

  async updateEventTicketTypeById(
    eventId,
    ticketId,
    updatePayload,
    authHeader,
  ) {
    try {
      const response = await lastValueFrom(
        this.httpService.patch(
          `${this.INVENTORY_URL}/events/${eventId}/ticket-types/${ticketId}`,
          updatePayload,
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );

      return response.data;
    } catch (error: any) {
      throw new HttpException(
        error.response.data.detail || 'Could not connect to Inventory Service',
        error.response.status || 500,
      );
    }
  }

  async deleteEventTicketTypeById(eventId, ticketId, authHeader) {
    try {
      const response = await lastValueFrom(
        this.httpService.delete(
          `${this.INVENTORY_URL}/events/${eventId}/ticket-types/${ticketId}`,
          {
            headers: {
              Authorization: authHeader,
            },
          },
        ),
      );

      return response.data;
    } catch (error: any) {
      throw new HttpException(
        error.response.data.detail || 'Could not connect to Inventory Service',
        error.response.status || 500,
      );
    }
  }
}

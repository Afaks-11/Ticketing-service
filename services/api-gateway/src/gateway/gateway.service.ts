import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class GatewayService {
  constructor(private readonly httpService: HttpService) {}

  async forwardRequest(url: string, method: string, body?: any) {
    const response = await firstValueFrom(
      this.httpService.request({
        url,
        method,
        data: body,
      }),
    );

    return response.data;
  }
}

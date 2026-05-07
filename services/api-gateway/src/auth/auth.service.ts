import { HttpException, Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom, catchError } from 'rxjs';
import { error } from 'console';

@Injectable()
export class AuthService {
  private authServiceUrl: string;

  constructor(
    private readonly httpService: HttpService,
    private readonly configService: ConfigService,
  ) {
    const authServiceUrl = this.configService.get<string>('AUTH_SERVICE_URL');

    if (!authServiceUrl) {
      throw new Error(' SYSTEM HALTED: please add AUTH_SERVICE_URL in .env');
    }

    this.authServiceUrl = authServiceUrl;
  }

  async login(loginDto: any) {
    const url = `${this.authServiceUrl}/api/auth/login`;

    // The firstValueFrom to convert NestJS's Observable into a standard Promise
    const { data } = await firstValueFrom(
      this.httpService.post(url, loginDto).pipe(
        catchError((error) => {
          throw new HttpException(
            error.response?.data?.message || 'Auth Service Error',
            error.response?.status || 500,
          );
        }),
      ),
    );

    return data;
  }

  async getMyProfile(authHeader: string) {
    const url = `${this.authServiceUrl}/api/users/me`;

    const { data } = await firstValueFrom(
      this.httpService
        .get(url, {
          headers: {
            Authorization: authHeader,
          },
        })
        .pipe(
          catchError((error) => {
            throw new HttpException(
              error.response.data.message || 'Auth Service Error',
              error.response.status || 500,
            );
          }),
        ),
    );
    return data;
  }

  async register(registerDto: any) {
     const url = `${this.authServiceUrl}/api/auth/register`;

  
    const { data } = await firstValueFrom(
      this.httpService.post(url, registerDto).pipe(
        catchError((error) => {
          throw new HttpException(
            error.response?.data?.message || 'Auth Service Error',
            error.response?.status || 500,
          );
        }),
      ),
    );

    return data;
  }
}

import {
  Controller,
  Get,
  Req,
  UnauthorizedException,
  UseGuards,
} from '@nestjs/common';
import { UsersService } from './users.service';
import { JwtAuthGuard } from 'src/common/auth.guard';

@UseGuards(JwtAuthGuard)
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get('/me')
  async getMyProfile(@Req() req: any) {
    const userId = req.user.id || req.user.sub;

    if (!userId) {
      throw new UnauthorizedException('User Id not found in token');
    }

    return this.usersService.findById(userId);
  }
}

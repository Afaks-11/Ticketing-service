import { IsUUID, IsInt, Min } from 'class-validator';

export class CreateOrderDto {
  @IsUUID()
  reservation_id!: string;

  @IsUUID()
  ticket_type_id!: string;

  @IsUUID()
  event_id!: string;

  @IsInt()
  @Min(1)
  quantity!: number;
}

import { pgTable, uuid, varchar, integer, numeric, timestamp, pgEnum } from 'drizzle-orm/pg-core'

export const orderStatusEnum = pgEnum('order_status', [
    'PENDING', 'COMPLETED', 'CANCELLED', 'REFUNDED'
])

export const orders = pgTable('orders', {
    id: uuid('id').primaryKey().defaultRandom(),
    userId: uuid('user_id').notNull(),
    reservationId: uuid('reservation_id').notNull(), 
    eventId: uuid('event_id').notNull(),
    ticketTypeId: uuid('ticket_type_id').notNull(),
    ticketQuantity: integer('ticket_quantity').notNull(),
    totalAmount: numeric('total_amount', { precision: 12, scale: 2}).notNull(),
    status: orderStatusEnum('status').default('PENDING').notNull(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
    updatedAt: timestamp('updated_at').defaultNow().notNull()
})
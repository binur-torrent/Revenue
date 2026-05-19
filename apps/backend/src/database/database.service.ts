import { Injectable, OnModuleDestroy } from '@nestjs/common'
import { Pool } from 'pg'

@Injectable()
export class DatabaseService extends Pool implements OnModuleDestroy {
  constructor() {
    super({
      host: 'localhost',
      port: 5432,
      user: 'postgres',
      password: 'postgres',
      database: 'revenue',
    })
  }

  async onModuleDestroy() {
    await this.end()
  }
}
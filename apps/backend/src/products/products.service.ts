import { Injectable } from '@nestjs/common';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { DatabaseService } from 'src/database/database.service';

@Injectable()
export class ProductsService {
  constructor(private readonly db: DatabaseService) {}

  async create(createProductDto: CreateProductDto) {
    const { name, price, stock, category } = createProductDto
  
    const result = await this.db.query(
      `
      INSERT INTO products (name, price, stock, category)
      VALUES ($1, $2, $3, $4)
      RETURNING *
      `,
      [name, price, stock, category],
    )
  
    return result.rows[0]
  }

  async findAll() {
    const result = await this.db.query(
      `SELECT * FROM products ORDER BY name ASC`,
    )
  
    return result.rows
  }

  findOne(id: number) {
    return `This action returns a #${id} product`;
  }

  update(id: number, updateProductDto: UpdateProductDto) {
    return `This action updates a #${id} product`;
  }

  remove(id: number) {
    return `This action removes a #${id} product`;
  }
}

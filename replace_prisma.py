import re

with open('README.md', 'r') as f:
    text = f.read()

# Update Tech Stack
text = text.replace('- Prisma\n- PostgreSQL', '- PostgreSQL (node-postgres / чистый SQL)')

# Update Architecture section with Data Flow
data_flow = """
### Как компоненты взаимодействуют между собой (Data Flow)

1. **Frontend (Next.js / Expo / Electron):** Пользователь нажимает кнопку (например, "Создать товар"). Клиентское приложение формирует JSON и отправляет HTTP POST запрос (REST API) на backend.
2. **Backend (NestJS Controller):** Принимает запрос, валидирует данные (DTO).
3. **Backend (NestJS Service):** Реализует бизнес-логику (проверяет права, формирует SQL-запрос).
4. **Database (PostgreSQL):** NestJS через библиотеку `pg` отправляет чистый SQL-запрос в базу данных. БД выполняет запрос и возвращает результат (записи).
5. **Backend (NestJS Response):** Сервис получает данные от БД, преобразует их при необходимости и контроллер возвращает HTTP ответ со статусом и JSON на frontend.
6. **Frontend:** Получает JSON и обновляет UI.
"""
text = text.replace('```\n\n---', '```\n' + data_flow + '\n---', 1)

# Phase 2 Header
text = text.replace('NestJS + Prisma + Postgres', 'NestJS + Postgres')

# Phase 2 Prisma Setup -> pg setup
text = text.replace('### STEP 2.3 — Prisma setup\n\n- Установить Prisma, подключить к Postgres\n- Первая миграция (пустая)\n- Понять разницу `prisma migrate dev` vs `prisma db push`', '### STEP 2.3 — PostgreSQL setup и миграции\n\n- Установить драйвер `pg` (node-postgres)\n- Настроить подключение через Connection Pool\n- Настроить инструмент миграций (например, `node-pg-migrate`)\n- Первая структурная миграция')

# Phase 2 Product model -> Product SQL Table
scala_str = """### STEP 2.4 — Product модель

Правильная Prisma schema (с прицелом на multi-tenant в PHASE 3 — `organizationId` добавим там):

```prisma
model Product {
  id        String   @id @default(cuid())
  name      String
  price     Decimal  @db.Decimal(12, 2)
  stock     Int      @default(0)
  category  String?
}
```"""
sql_str = """### STEP 2.4 — Product SQL Table

Заложить структуру с прицелом на multi-tenant в PHASE 3 (внешний ключ `organization_id` добавим там):

```sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  price DECIMAL(12, 2) NOT NULL,
  stock INT DEFAULT 0,
  category VARCHAR(255)
);
```"""
text = text.replace(scala_str, sql_str)

# Phase 2 What I will learn
text = text.replace('Prisma queries и миграции', 'Конструирование чистых SQL запросов и управление пулом соединений')

# Phase 3 User and Org model
schema2_str = """### STEP 3.1 — User и Organization модели

```prisma
model Organization {
  id        String   @id @default(cuid())
  name      String
  createdAt DateTime @default(now())
  users     User[]
  products  Product[]
}

model User {
  id             String       @id @default(cuid())
  email          String       @unique
  passwordHash   String
  role           Role         @default(EMPLOYEE)
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id])
}

enum Role {
  OWNER
  ADMIN
  EMPLOYEE
}
```"""

sql2_str = """### STEP 3.1 — User и Organization SQL Tables

```sql
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE user_role AS ENUM ('OWNER', 'ADMIN', 'EMPLOYEE');

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role user_role DEFAULT 'EMPLOYEE',
  organization_id UUID REFERENCES organizations(id)
);
```"""
text = text.replace(schema2_str, sql2_str)

# Phase 4
text = text.replace('Transactions в Prisma', 'SQL Transactions (BEGIN, COMMIT, ROLLBACK)')

# Decisions log
text = text.replace('| 2026-05-11 | Prisma                           | Drizzle / TypeORM | Лучшая документация для новичка       |', '| 2026-05-19 | node-postgres (чистый SQL)       | Prisma / TypeORM  | Решил писать чистый SQL для контроля и глубокого понимания таблиц и запросов |')

with open('README.md', 'w') as f:
    f.write(text)


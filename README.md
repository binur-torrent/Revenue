# Revenue — ERP система

Полный roadmap разработки fullstack ERP системы. Документ для себя: план, решения, прогресс.

---

## Главная цель проекта

Построить полноценную ERP систему с:

- desktop приложением (главный клиент)
- мобильным приложением (companion для админов и владельцев)
- SaaS веб-сайтом (landing + подписки + регистрация)
- единым backend для всех клиентов
- multi-tenant архитектурой (поддержка нескольких бизнесов)
- возможностью масштабирования

При этом параллельная (и более важная) цель:

- научиться fullstack разработке
- изучить TypeScript на практике
- понять архитектуру больших систем
- научиться строить и доводить до конца реальные продукты

> **Главное правило:** AI помогает объяснять, ревьюить, направлять. AI **не пишет** систему за меня. Каждая строка кода должна быть понята.

---

## Prerequisites — что нужно знать до старта

Базовые знания, без которых дальше будет больно:

- **TypeScript** — типы, интерфейсы, generics, narrowing, utility types
- **JavaScript runtime** — async/await, Promises, event loop (концептуально)
- **HTTP / REST** — методы, статус коды, JSON, что такое API
- **SQL** — SELECT, JOIN, WHERE, primary/foreign keys, indexes (до Prisma)
- **Git** — branches, merge, rebase, осмысленные коммиты
- **Терминал** — базовые команды, переменные окружения

Если что-то проседает — подтянуть до начала соответствующей фазы.

---

## Стек проекта

### Frontend (web + desktop UI)

- TypeScript
- React
- Next.js (App Router)
- Tailwind CSS
- shadcn/ui

### Backend

- NestJS
- PostgreSQL (node-postgres / чистый SQL)

### Infrastructure

- Docker / Docker Compose

### Desktop

- Electron (решение пересмотреть в PHASE 5, см. Decisions log)

### Mobile

- Expo + React Native

### Tooling

- pnpm (package manager)
- ESLint + Prettier
- Bruno или Postman (тестирование API)

---

## Архитектура системы

Все клиенты работают параллельно и обращаются к одному API.

```txt
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Desktop    │   │   Mobile     │   │   Web SaaS   │
│  (Electron)  │   │   (Expo)     │   │  (Next.js)   │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          ▼
                  ┌───────────────┐
                  │ API (NestJS)  │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │  PostgreSQL   │
                  └───────────────┘
```

### Как компоненты взаимодействуют между собой (Data Flow)

1. **Frontend (Next.js / Expo / Electron):** Пользователь нажимает кнопку (например, "Создать товар"). Клиентское приложение формирует JSON и отправляет HTTP POST запрос (REST API) на backend.
2. **Backend (NestJS Controller):** Принимает запрос, валидирует данные (DTO).
3. **Backend (NestJS Service):** Реализует бизнес-логику (проверяет права, формирует SQL-запрос).
4. **Database (PostgreSQL):** NestJS через библиотеку `pg` отправляет чистый SQL-запрос в базу данных. БД выполняет запрос и возвращает результат (записи).
5. **Backend (NestJS Response):** Сервис получает данные от БД, преобразует их при необходимости и контроллер возвращает HTTP ответ со статусом и JSON на frontend.
6. **Frontend:** Получает JSON и обновляет UI.

---

## Структура репозитория

```txt
revenue/
  apps/
    web/         # Next.js — landing + ERP веб-панель
    backend/     # NestJS API
    desktop/     # Electron wrapper (появится в PHASE 5)
    mobile/      # Expo приложение (появится в PHASE 7)

  packages/
    shared-types/  # общие TS типы между клиентами и backend (опционально)

  docker/
    docker-compose.yml
```

> На раннем этапе монорепо может быть избыточным. Если pnpm workspaces тормозят обучение — допустимо начать с двух отдельных папок и объединить позже.

---

## Definition of Done

Фича считается завершённой, когда:

- [ ] Код написан и понят (могу объяснить каждую строку)
- [ ] Нет `any` в TypeScript без явного обоснования
- [ ] Проходит линтер без ошибок
- [ ] Ручной happy-path сценарий проверен
- [ ] Для backend: есть хотя бы базовый unit-тест сервиса
- [ ] Коммит с осмысленным сообщением (см. ниже)
- [ ] Замержено в `main`

### Формат коммитов

`<type>: <короткое описание>` — например:

- `feat: add products CRUD endpoints`
- `fix: handle empty stock in inventory service`
- `docs: update roadmap with auth phase`
- `chore: scaffold monorepo structure`
- `refactor: extract product validation to DTO`

Никаких `"Initial commit"`, `"update"`, `"fix bug"` без контекста.

---

## Подход к тестированию

Не TDD, но и не "никогда". По фазам:

- **PHASE 1–2:** ручное тестирование (Bruno / Postman) — допустимо
- **PHASE 3+:** unit тесты для сервисов NestJS (auth, multi-tenant — обязательно)
- **PHASE 4+:** e2e тесты основных flow (создание заказа, проверка остатков)
- **PHASE 5+:** smoke тесты на desktop сборку перед релизом

---

# PHASE 1 — Frontend foundation

**Цель:** запустить Next.js, освоить базовый layout, понять App Router и shadcn/ui. Никакого backend.

### STEP 1.1 — Инициализация проекта

- Создать `apps/web` через `create-next-app` (TypeScript, App Router, Tailwind, ESLint)
- Запустить dev server, убедиться что работает
- Настроить ESLint + Prettier
- Первый осмысленный коммит

### STEP 1.2 — shadcn/ui setup

- Запустить `shadcn init`
- Установить базовые компоненты: `button`, `input`, `card`, `dropdown-menu`
- Понять, что shadcn копирует код в проект, а не ставится как пакет

### STEP 1.3 — Layout, Sidebar, TopBar

- Запроектировать layout на бумаге **до** кода
- Реализовать в `app/layout.tsx`
- Sidebar — отдельный компонент, список пунктов через массив-конфиг
- TopBar — отдельный компонент
- Иконки через `lucide-react`

### STEP 1.4 — Навигация и пустые страницы

- `<Link>` из `next/link` (не `<a>`)
- Подсветка активного пункта через `usePathname()`
- Создать пустые страницы: Dashboard, Products, Orders, Inventory, Customers

### Что изучу на этом этапе

- Next.js App Router, layouts vs pages
- Server vs Client components
- Tailwind utility-first подход
- React component composition
- TypeScript в реальном проекте

---

# PHASE 2 — Backend foundation + первый CRUD

**Цель:** поднять NestJS + Postgres, реализовать первую сущность (`Product`) с реальным API. Подключить к frontend.

### STEP 2.1 — Postgres в Docker

- `docker-compose.yml` с сервисом postgres
- Подключиться через DBeaver или `psql`
- Понять volumes, ports, env variables

### STEP 2.2 — NestJS scaffold

- `nest new` в `apps/backend`
- Структура: modules / controllers / services / DTOs
- Базовый health endpoint

### STEP 2.3 — PostgreSQL setup и миграции

- Установить драйвер `pg` (node-postgres)
- Настроить подключение через Connection Pool
- Настроить инструмент миграций (например, `node-pg-migrate`)
- Первая структурная миграция

### STEP 2.4 — Product SQL Table

Заложить структуру с прицелом на multi-tenant в PHASE 3 (внешний ключ `organization_id` добавим там):

```sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  price DECIMAL(12, 2) NOT NULL,
  stock INT DEFAULT 0,
  category VARCHAR(255)
);
```

> `price` — обязательно `Decimal`, не `Float`. Float теряет точность на деньгах.

### STEP 2.5 — Products module в NestJS

- `ProductsModule`, `ProductsService`, `ProductsController`
- DTO с валидацией через `class-validator`
- CRUD endpoints: GET list, GET by id, POST, PATCH, DELETE
- Первый unit тест сервиса

### STEP 2.6 — Подключение frontend ↔ backend

- Реализовать `Products` страницу с реальной таблицей
- `fetch` или `tanstack-query` (рекомендую второе)
- Форма добавления, редактирования, удаления
- CORS настройка в Nest

### Что изучу

- NestJS архитектура (DI, modules, providers)
- Конструирование чистых SQL запросов и управление пулом соединений
- DTO и валидация на бэке
- HTTP клиент на фронте
- async/await на практике
- Server Components vs Client Components для data fetching

---

# PHASE 3 — Authentication + Multi-tenancy

> Эту фазу нельзя откладывать. Если добавить `organizationId` через год — будет катастрофическая миграция.

**Цель:** регистрация, логин, организации, изоляция данных.

### STEP 3.1 — User и Organization SQL Tables

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
```

### STEP 3.2 — Добавить `organizationId` ко всем существующим таблицам

- `Product` получает `organizationId`
- Миграция с дефолтным значением для существующих записей
- Тестовая seed-данные

### STEP 3.3 — Auth в NestJS

- Хэширование паролей через `argon2`
- JWT (access + refresh tokens)
- `AuthModule`, `AuthService`, `AuthController`
- Guards: `JwtAuthGuard`, `RolesGuard`

### STEP 3.4 — Tenant isolation

- Middleware / interceptor, который извлекает `organizationId` из JWT
- Все queries автоматически фильтруются по `organizationId`
- Тесты, проверяющие что пользователь не видит чужие данные

### STEP 3.5 — Login / Register на frontend

- Страницы `/login`, `/register`
- Хранение токенов (HttpOnly cookies предпочтительнее localStorage)
- Защищённые routes через middleware Next.js
- Logout

### Что изучу

- JWT, refresh token flow
- Хэширование паролей
- Authorization vs Authentication
- Multi-tenancy паттерны
- Защита API endpoints
- Безопасное хранение токенов на клиенте

---

# PHASE 4 — Core ERP модули

**Цель:** довести веб-панель до состояния минимально полезной ERP.

### Inventory

- Stock tracking
- Stock updates (приход / расход)
- Warehouse quantities (если будет несколько складов — позже)

### Orders

- Создание заказа (с несколькими позициями)
- История заказов
- Автоматическое уменьшение stock при создании заказа (в транзакции)
- Статусы: DRAFT, CONFIRMED, FULFILLED, CANCELLED

### Customers

- CRUD клиентов
- История покупок клиента
- Контактная информация

### Dashboard

- Sales analytics (выручка по периодам)
- Total revenue
- Low stock alerts
- Топ товары

### Что изучу

- Database relations (one-to-many, many-to-many)
- SQL Transactions (BEGIN, COMMIT, ROLLBACK)
- Aggregation queries
- Сложный state на frontend
- Графики (recharts / tremor)

---

# PHASE 5 — Desktop приложение

**Цель:** превратить веб-панель в нативное desktop приложение.

### Открытые архитектурные вопросы (решить в начале фазы)

1. Electron запускает локальный Next.js сервер, или грузит production-build?
2. Или это отдельный React app, специально собранный для Electron?
3. Использовать Electron или пересмотреть выбор в пользу Tauri?

Решение зафиксировать в Decisions log.

### Что делать

- Создать `apps/desktop` с Electron
- Загрузить веб-панель внутрь
- Auto-update механизм
- Подписать сборки (для macOS / Windows)

### Desktop-only функции

- Receipt printing (печать чеков)
- Barcode scanner support
- File export/import (CSV, Excel)
- Offline caching (sync при восстановлении сети)
- Desktop notifications

---

# PHASE 6 — SaaS Website + Billing

**Цель:** маркетинговый сайт + регистрация бизнеса + платная подписка.

### Pages

- Landing
- Pricing
- Features
- Contact
- Login / Register (уже есть с PHASE 3 — переиспользовать)

### Billing

- Stripe (или Paddle) для подписок
- Webhooks для обновления статуса подписки
- Привязка подписки к `Organization`
- Trial period
- Plan limits (например, лимит на количество продуктов)

### Email

- Resend или Postmark
- Email verification
- Сброс пароля
- Уведомления о платежах

---

# PHASE 7 — Mobile приложение

**Цель:** companion app для владельцев и админов.

> **Ограничение, которое нельзя нарушать:** mobile никогда не должен быть полной заменой desktop. Если фича сложнее одного экрана — она не для mobile.

### Stack

- Expo + React Native + TypeScript

### Read-only функции

- Sales и revenue dashboard
- Inventory check
- Notifications
- Просмотр истории действий сотрудников

### Limited actions

- Approve / reject запросов
- Базовые отчёты
- Мониторинг сотрудников

---

# PHASE 8 — Advanced ERP функции

Добавлять постепенно, по мере реальной необходимости.

### Finance

- Транзакции
- Расходы
- Финансовые отчёты

### POS

- Кассовый интерфейс
- Чеки
- Смены кассиров

### Employees

- Расширенные права доступа
- Расписания
- История действий (audit log)

### Warehouse

- Перемещения между складами
- Списания
- Инвентаризация

---

# PHASE 9 — Scaling architecture

> Только после стабильного MVP и реальных пользователей. Не раньше.

### Infrastructure

- Redis (кеш + сессии)
- BullMQ или аналог для очередей
- Background jobs (отчёты, email)

### Architecture

- Выделение микросервисов, если монолит реально не справляется
- Event-driven подход где уместно
- WebSockets для real-time sync клиентов

### Deployment

- CI/CD pipeline (GitHub Actions)
- Monitoring (Sentry, Grafana)
- Logging (структурированные логи)
- Backup стратегия для Postgres

---

## Decisions log

Короткие записи "почему выбрал X, а не Y". Заполнять по мере принятия решений.

| Дата       | Решение                          | Альтернатива      | Причина                               |
| ---------- | -------------------------------- | ----------------- | ------------------------------------- |
| 2026-05-11 | Next.js App Router               | Pages Router      | Современный подход, server components |
| 2026-05-11 | NestJS для backend               | Express / Fastify | Структура подходит для ERP (модули)   |
| 2026-05-19 | node-postgres (чистый SQL)       | Prisma / TypeORM  | Решил писать чистый SQL для контроля и глубокого понимания таблиц и запросов |
| 2026-05-11 | Electron (пока)                  | Tauri             | Проще на старте, пересмотр в PHASE 5  |
| 2026-05-11 | Multi-tenant с PHASE 3, не позже | Добавить позже    | Миграция данных потом — катастрофа    |

---

## Local development setup

> Заполнять по мере того, как окружение реально поднимется.

```bash
# TODO: clone, install, env, docker-compose up, migrate, dev
```

---

## Как использовать AI в этом проекте

### AI помогает

- объяснять концепции
- ревьюить код
- разбирать ошибки
- обсуждать архитектурные решения
- указывать на проблемы, которые я не вижу

### AI НЕ должен

- писать систему за меня
- генерировать большие куски кода, которые я не понимаю
- принимать архитектурные решения вместо меня
- "просто чинить" — должен объяснять, что было не так

---

## Главное правило проекта

Не пытаться:

- сделать идеально
- использовать все технологии сразу
- строить enterprise architecture с первого дня

Главная цель:

- завершать фичи до конца (Definition of Done)
- понимать каждую часть системы
- учиться через практику и осознанные ошибки
- видеть результат своей работы

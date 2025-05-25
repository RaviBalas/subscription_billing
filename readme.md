# Subscription Billing System

A Django-based subscription billing system that manages users, subscriptions, invoices, and payments. The system includes features like user authentication, subscription management, invoice generation, and payment processing.

## Features

- **User Management**: User registration, login, and authentication using JWT.
- **Subscription Management**: Users can subscribe to plans, cancel subscriptions, and view active subscriptions.
- **Invoice Management**: Automatic invoice generation for active subscriptions, overdue invoice tracking, and payment processing.
- **Task Scheduling**: Celery tasks for generating invoices, marking overdue invoices, and sending reminders.
- **Dockerized**: Easily deployable using Docker and Docker Compose.

---

## Installation

### Prerequisites

- Python 3.13
- Docker
- Redis
- PostgreSQL

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/RaviBalas/subscription_billing.git
   cd subscription_billing
   ```
2. Set up the environment (`.env`) file:
   ```
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   THROTTLE_LIMIT_PER_MINUTE=20
   SECRET_KEY=<secret-key>
   POSTGRES_DB=<dev_name>
   POSTGRES_USER=<username>
   POSTGRES_PASSWORD=<password>
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   REDIS_HOST=redis
   REDIS_PORT=6379
   ACCESS_TOKEN_LIFETIME_IN_MINUTE=1440
   REFRESH_TOKEN_LIFETIME_IN_MINUTE=10080
   CURRENT_DB=postgres
   ```

3. Build the Docker image:
   ```
   docker compose build
   ```

4. Run the Docker containers:
   ```bash
   docker compose up 
   ```

5. Access the backend container:
   ```bash
   docker exec -it subscription_billing_backend bash
   ```

6. Load initial data into the database:
   ```bash
   python manage.py loaddata initial_fixtures.json
   ```
---
7. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

---

## API Endpoints

### User Endpoints
- **POST** `/auth/registration/`: Register a new user.
- **POST** `/auth/login/`: Login and obtain JWT tokens.

### Subscription Endpoints
- **GET** `/subscription/plans/`: List all subscription plans.
- **POST** `/subscription/subscribe/`: Subscribe to a plan.
- **POST** `/subscription/unsubscribe/`: Unsubscribe from a plan.

### Invoice Endpoints
- **GET** `/invoice/my_invoices/`: List all invoices for the logged-in user.
- **POST** `/invoice/<invoice_id>/payment`: Pay an invoice.

---

## Celery Tasks

- **Generate Invoices**: Automatically generates invoices for active subscriptions.
- **Mark Overdue Invoices**: Marks unpaid invoices as overdue.
- **Send Reminder Emails**: Sends reminder emails for pending invoices.

To start the Celery worker and start the Celery beat scheduler:
```bash
celery  -A core worker --loglevel=INFO --autoscale=1,1  -Q main_queue -B
```
---

## Testing

Run the test suite using:
```bash
python manage.py test
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
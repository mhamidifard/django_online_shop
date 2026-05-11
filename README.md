# 🛒 Modular E-Commerce REST API

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-092E20.svg)
![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D.svg)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12-FF6600.svg)
![Celery](https://img.shields.io/badge/Celery-5.3-37814A.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A highly modular, scalable, and production-ready e-commerce RESTful API backend built with Django and Django REST Framework. This project is inspired by the architecture of leading e-commerce platforms like Digikala, demonstrating advanced concepts in system design, caching strategies, asynchronous processing, and clean code principles.

---

## 🏗️ Project Architecture & Structure

The project follows a modular, app-based architecture to ensure separation of concerns and maintainability.

*   **`accounts/`**: Handles user authentication and authorization using a Custom User model and JWT (JSON Web Tokens).
*   **`products/`**: Manages the product catalog, including hierarchical categories, product variants (e.g., size, color), and multiple product images.
*   **`cart/`**: Handles session-based and authenticated user shopping cart logic.
*   **`orders/`**: Manages the checkout process, order creation, and status tracking.
*   **`product_reviews/`**: Allows authenticated users to leave ratings and reviews for products.

---

## 🚀 Key Features

*   **Asynchronous Task Processing**: Integrated with **Celery** and **RabbitMQ** to handle background tasks asynchronously, such as sending email notifications and processing orders without blocking the main web thread.
*   **Advanced Caching Strategy**: Utilizes **Redis** for high-performance data caching. Implements advanced patterns like **Jitter** to prevent Cache Stampede issues during high traffic and cache expirations.
*   **Production-Ready Dockerization**: Fully containerized environment orchestrated with Docker Compose. Services include:
    *   Web Server (Django/Gunicorn)
    *   Celery Worker
    *   Celery Beat (Scheduled tasks)
    *   Flower (Celery monitoring)
    *   Redis (Cache & Message Broker)
    *   RabbitMQ (Message Broker)
    *   PostgreSQL (Primary Database)
*   **Interactive API Documentation**: Automated, OpenAPI 3.0 compliant documentation generated via `drf-spectacular`, accessible via Swagger UI and ReDoc.
*   **Robust Authentication**: Secure stateless authentication via JWT tokens.

---

## 🛠️ Tech Stack

*   **Framework**: Django 5.2, Django REST Framework (DRF)
*   **Database**: PostgreSQL
*   **Cache & Broker**: Redis, RabbitMQ
*   **Task Queue**: Celery
*   **Containerization**: Docker, Docker Compose
*   **Testing**: Pytest, factory_boy, pytest-django
*   **Documentation**: drf-spectacular (Swagger)

---

## ⚙️ Installation & Setup

The easiest way to run the application is using Docker. Ensure you have Docker and Docker Compose installed on your system.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mhamidifard/Modular-E-Commerce-REST-API.git
    cd Modular-E-Commerce-REST-API
    ```

2.  **Environment Variables:**
    Create a `.env` file in the root directory based on the provided `.env.example` file and configure your database and secret keys.

3.  **Build and Run with Docker Compose:**
    ```bash
    docker compose up --build
    ```
    This single command will build the images, create the database, run migrations, start the background workers, and launch the API server.

4.  **Access the Application:**
    *   API Server: `http://localhost:8000/`
    *   Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
    *   Flower Dashboard: `http://localhost:5555/`

---

## 🧪 Development & Testing

Quality assurance is maintained through a comprehensive test suite.

*   **Tools**: Built entirely with `pytest`, leveraging `pytest-django` for seamless framework integration.
*   **Data Generation**: Uses `factory_boy` to create modular, maintainable, and realistic test data factories.
*   **Environments**: The project uses modular settings configurations to strictly separate Development, Testing, and Production environments.

**Running Tests Locally (inside the container):**
```bash
docker compose exec web pytest
```

---

## 📖 API Documentation

![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white) ![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-85EA2D?style=for-the-badge&logo=openapi-initiative&logoColor=white)

This API is fully documented using the **OpenAPI 3.0** specification. The documentation is auto-generated and maintained via the `drf-spectacular` package, ensuring it stays perfectly in sync with the codebase.

*   📄 **Local Schema File:** [openapi-schema.yaml](./openapi-schema.yaml)
*   🌐 **Interactive Viewer:** [View Schema in Swagger Editor](https://editor.swagger.io/?url=https://raw.githubusercontent.com/mhamidifard/Modular-E-Commerce-REST-API/master/openapi-schema.yaml)

### 🔄 Regenerating the Schema Locally

Whenever you make changes to your API views or serializers, you can regenerate the local schema file by running the following command:

```bash
python manage.py spectacular --file openapi-schema.yaml
```

---

## 📡 API Endpoints Overview

Below is a detailed summary of the actual core API endpoints implemented in this project, generated directly from our OpenAPI schema.

### 🔐 Authentication (`/api/auth/`)
*   **`POST /api/auth/login/`**: Authenticate user credentials and return JWT tokens.
*   **`POST /api/auth/logout/`**: Blacklist a refresh token and log out the current user.
*   **`POST /api/auth/register/`**: Register a new user and return profile plus JWT token pair.
*   **`POST /api/auth/password-reset/`**: Request a password reset link by email (rate limited).
*   **`POST /api/auth/password-reset/confirm/`**: Reset password using `uid`, `token`, and a new password.
*   **`GET /api/auth/test-authentication/`**: Validate the current JWT access token and return authentication state.

### 🛍️ Product Catalog (`/api/products/`)
*   **`GET /api/products/`**: List all products (paginated).
*   **`POST /api/products/add/`**: Create a new product with variants.
*   **`GET /api/products/{id}/`**: Retrieve detailed product information with variants and images.
*   **`PUT /api/products/{id}/update/`**: Fully update a product.
*   **`PATCH /api/products/{id}/update/`**: Partially update a product.
*   **`DELETE /api/products/{id}/delete/`**: Delete a product.

### 🖼️ Product Images (`/api/images/`)
*   **`POST /api/products/{product_id}/images/upload/`**: Upload an image for a product.
*   **`DELETE /api/images/{id}/delete/`**: Delete a specific product image.

### 📁 Categories (`/api/categories/`)
*   **`GET /api/categories/`**: List root categories with nested children.
*   **`GET /api/categories/{slug}/`**: Retrieve a category by its slug.

### ⭐ Reviews (`/api/products/{product_id}/reviews/`)
*   **`GET /api/products/{product_id}/reviews/`**: List paginated reviews for a specific product.
*   **`POST /api/products/{product_id}/reviews/add/`**: Create a product review for the authenticated user.
*   **`DELETE /api/products/reviews/{id}/delete/`**: Delete the current user's review.

### 🛒 Shopping Cart (`/api/cart/`)
*   **`GET /api/cart/`**: Get the authenticated user's cart.
*   **`POST /api/cart/add/`**: Add an item to the cart or increase quantity.
*   **`PUT /api/cart/update/{id}/`**: Update cart item quantity.
*   **`PATCH /api/cart/update/{id}/`**: Partially update cart item quantity.
*   **`DELETE /api/cart/remove/{id}/`**: Remove an item from the cart.

### 📦 Orders (`/api/orders/`)
*   **`POST /api/convert-cart-to-order/`**: Convert authenticated user's cart into an order.
*   **`GET /api/orders/`**: List authenticated user's orders (paginated).
*   **`GET /api/orders/{id}/`**: Retrieve detailed order information.
*   **`PATCH /api/orders/{id}/update-status/`**: Update order status (Admin only).

---

## 📜 License

This project is licensed under the MIT License.

---

*Designed and developed to demonstrate scalable backend engineering practices and production-ready system architecture.*

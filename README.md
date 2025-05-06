# Ship Dispatch API

A FastAPI-based system for monitoring and analyzing ship movements to assess the risk of maritime collisions.

📦 Repository: https://github.com/maymeskul123/ship-dispatch-api

---

## 🚀 Features

- Ships report their current position and time
- The system calculates their speed and trajectory
- Evaluates the risk of collision within 60 seconds
- Returns one of three statuses: `green`, `yellow`, or `red`
- API endpoints to view all ships, individual ship history, and reset the data

---

## 🐳 Running the App with Docker

Ensure you have Docker and Docker Compose installed.

### 🟢 Start the API server

```bash
docker compose up
```

- The API will be available at: [http://localhost:8080/docs](http://localhost:8080/docs)
- Swagger UI provides full interactive API documentation

---

## ✅ Running Tests

To run unit tests using Pytest inside Docker:

```bash
docker compose run test
```

Test files are located in the `tests/` folder.

---

## 🧪 API Overview

### POST /v1/api/ships/{id}/position

Report a ship's current position and time.

**Request Body:**

```json
{
  "time": 1744383218,
  "x": 2,
  "y": 3
}
```

**Response:**

```json
{
  "time": 1744383218,
  "x": 2,
  "y": 3,
  "speed": 0.0,
  "status": "green"
}
```

---

### GET /v1/api/ships

Get status of all known ships.

---

### GET /v1/api/ships/{id}

Get full position history for a specific ship.

---

### POST /v1/api/flush

Clear all stored data (for testing and development).

---

## 📂 Project Structure

```
.
├── main.py                 # FastAPI app
├── tests/
│   └── test_api.py         # Example unit test
├── Dockerfile              # Container image setup
├── docker-compose.yml      # Defines app and test services
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🧰 Useful Docker Commands

- **Build manually (if needed):**

  ```bash
  docker compose build
  ```

- **Rebuild and start fresh:**

  ```bash
  docker compose up --build
  ```

- **Shut down containers:**

  ```bash
  docker compose down
  ```

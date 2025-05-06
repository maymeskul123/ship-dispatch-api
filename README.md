# Ship Coordination Dispatch Service

## 🚢 Description

This service tracks ship movements and predicts potential collisions in open waters using a RESTful API.

## ✅ Requirements Met

- FastAPI backend
- REST API with the specified endpoints
- Validations for time and coordinates
- Collision prediction logic
- Dockerized deployment
- Accessible at http://localhost:8080

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone <your_repo_url>
   cd <your_repo>

# Ship Dispatch API

A FastAPI-based backend to track ship positions and assess maritime collision risks.

📍 GitHub Repository: [https://github.com/maymeskul123/ship-dispatch-api](https://github.com/maymeskul123/ship-dispatch-api)

## 🚢 Features

- Accepts real-time ship coordinates via REST API
- Calculates speed and movement direction
- Evaluates potential collision risks over the next 60 seconds
- Provides status: `green`, `yellow`, or `red`
- Keeps full position history per ship
- Supports test flushing via `/flush`

---

## 🚀 Run the App (Docker)

Make sure you have Docker and Docker Compose installed.

### Start API server:

```bash
docker compose up

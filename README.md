# 🔗 URL Shortener — Backend

A REST API for shortening URLs, built with FastAPI. Supports user authentication, custom aliases, and automatic short code generation.

## ✨ Features

- **Shorten URLs** — generates a unique 7-character short code using base62 encoding
- **Custom aliases** — users can define their own short code
- **User auth** — JWT-based signup and login
- **Redirect** — visiting `/{short_code}` redirects to the original URL
- **Duplicate detection** — returns existing short URL if the same URL was already shortened by the user

## 🚀 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/signup` | Register a new user |
| `POST` | `/auth/login` | Login and get JWT token |
| `POST` | `/shorten` | Shorten a URL (auth required) |
| `GET` | `/{short_code}` | Redirect to original URL |

## 🛠️ Tech Stack

- **Python**
- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **PostgreSQL** — database
- **JWT** — authentication
- **Docker + Nginx** — containerized deployment

## 📁 Project Structure

```
app/
├── main.py          # Entry point, routes
├── models.py        # Database models
├── schemas.py       # Pydantic schemas
├── crud.py          # Database operations
├── auth.py          # JWT auth logic
├── database.py      # DB connection
└── dependencies.py  # Auth dependencies
```

## ⚙️ Setup

1. Clone the repo
2. Create a `.env` file:
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=your_secret_key_here
   ```
3. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

Or without Docker:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

## 👤 Author

Made by [@lol_wave](https://t.me/lol_wave)

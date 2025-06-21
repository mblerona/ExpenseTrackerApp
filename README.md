# Expense Tracker App

This is a full-stack simple expense tracker app built with Flask and MongoDB for my DevOps course.

## Tech Used for this project 
- Backend: Flask (Python)
- Frontend: Flask serving HTML/JS
- Database: MongoDB
- CI/CD: GitHub Actions + Docker + Docker Hub

## CI/CD Pipeline
Every push to the `master` branch triggers a GitHub Actions workflow that:
- Builds Docker images for backend and frontend
- Pushes them to Docker Hub

## Docker Hub Links
- [Backend Image](https://hub.docker.com/r/yourusername/expense-tracker-backend)
- [Frontend Image](https://hub.docker.com/r/yourusername/expense-tracker-frontend)

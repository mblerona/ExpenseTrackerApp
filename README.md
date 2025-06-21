# Expense Tracker App

A full-stack simple Expense Tracking web application built with Flask, MongoDB, and deployed using Docker, Kubernetes, and GitHub Actions.

---

##  Tech Used

- **Frontend**: Flask + HTML/JS (served as a separate container)
- **Backend**: Flask REST API with `/expenses` and `/stats`
- **Database**: MongoDB (StatefulSet in Kubernetes)
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Orchestration**: Docker Compose and Kubernetes (via k3d)
- **Ingress**: Traefik (through k3d)

---

##  Features

- Add, view, and list expenses
- Monthly average per category
- MongoDB-backed persistence
- Frontend and backend separated into services
- CI pipeline with Docker image build and push
- Fully deployed to Kubernetes

---

##  GitHub Actions CI/CD

Every push to `master` triggers:

-  Docker build for backend and frontend
-  Push to Docker Hub
-  (CD step done manually via `kubectl apply`)

CI pipeline defined in:

```
.github/workflows/docker.yml
```

---

##  Docker Hub Images

- [`rona03/expense-tracker-backend`](https://hub.docker.com/r/rona03/expense-tracker-backend)
- [`rona03/expense-tracker-frontend`](https://hub.docker.com/r/rona03/expense-tracker-frontend)

---

##  Run Locally (Docker Compose)

```bash
docker-compose up --build
```

Then visit:  
[http://localhost:8080](http://localhost:8080)

---

##  Kubernetes Deployment (k3d)

### 🔹 Step 1: Create Cluster with Port Mapping

```bash
k3d cluster create expense-cluster -p "8081:80@loadbalancer"
```

---

### 🔹 Step 2: Add Custom Domain to Hosts File

In `C:\Windows\System32\drivers\etc\hosts`, add:

```
127.0.0.1 expense.local
```

---

### 🔹 Step 3: Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/
```

> If namespace timing errors occur:
```bash
kubectl apply -f k8s/deployment-backend.yml
kubectl apply -f k8s/deployment-frontend.yml
kubectl apply -f k8s/ingress.yml
```

---

### 🔹 Step 4: Access the App

```
http://expense.local:8081
```

---

##  Kubernetes Manifest Overview

All resources live inside the `expense-tracker` namespace.

```
k8s/
├── namespace.yml                # Defines custom namespace
├── backend-deployment.yml
├── frontend-deployment.yml
├── mongo-statefulset.yml
├── backend-service.yml
├── frontend-service.yml
├── mongo-service.yml
└── ingress.yml                  # Ingress using Traefik via k3d
```

---

##  Verify Kubernetes Deployment

```bash
kubectl get ns
kubectl get pods -n expense-tracker
kubectl get svc -n expense-tracker
kubectl get ingress -n expense-tracker
```

---

##  Access Stats (API)

### Backend `/stats` endpoint:

```bash
kubectl port-forward svc/backend 5000:5000 -n expense-tracker
```

Then visit:
```
http://localhost:5000/stats
```

---

# Deployment Guide

## Overview
This Django ecommerce application is containerized with Docker and configured for deployment on Render.com with CI/CD via GitHub Actions.

## Local Development with Docker

### Prerequisites
- Docker and Docker Compose installed
- Git repository

### Running Locally
```bash
# Build and start services
docker-compose up --build

# Run migrations (first time)
docker-compose exec web python manage.py migrate

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

Access the application at http://localhost:8000

## Deployment on Render

### Step 1: Prepare Repository
1. Push your code to GitHub
2. Ensure all files are committed including:
   - `Dockerfile`
   - `render.yaml`
   - `.github/workflows/deploy.yml`

### Step 2: Create Render Account
1. Sign up at [render.com](https://render.com)
2. Connect your GitHub account

### Step 3: Deploy Database
1. Go to Render Dashboard
2. Click "New" → "PostgreSQL"
3. Name: `ecommerce-db`
4. Database Name: `ecommerce`
5. User: `ecommerce`
6. Note the connection string for later

### Step 4: Deploy Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Choose "Deploy from Docker"
4. Set environment variables:
   - `SECRET_KEY`: Generate a secure key
   - `DEBUG`: False
   - `RENDER`: True
   - `DATABASE_URL`: Your PostgreSQL connection string

### Step 5: Configure CI/CD
1. In GitHub repository, go to Settings → Secrets and variables → Actions
2. Add secrets:
   - `RENDER_SERVICE_ID`: Your Render service ID
   - `RENDER_API_KEY`: Your Render API key

## CI/CD Pipeline

The GitHub Actions workflow (`deploy.yml`) automatically:
1. **Tests**: Runs Django tests with PostgreSQL
2. **Build**: Creates Docker image and pushes to GitHub Container Registry
3. **Deploy**: Triggers deployment on Render

Pipeline triggers on:
- Push to `main` branch
- Pull requests to `main` branch

## Environment Variables

### Required for Production
- `SECRET_KEY`: Django secret key (auto-generated on Render)
- `DATABASE_URL`: PostgreSQL connection string
- `DEBUG`: Set to `False`
- `RENDER`: Set to `True`

### Optional
- `RENDER_EXTERNAL_HOSTNAME`: Auto-set by Render

## Static Files
- Handled by WhiteNoise middleware
- Collected automatically during deployment
- Stored in `/app/staticfiles` directory

## Database Migrations
- Run automatically during deployment via Dockerfile CMD
- Can be run manually: `python manage.py migrate`

## Monitoring
- Check logs in Render dashboard
- Monitor database performance
- Set up alerts for downtime

## Troubleshooting

### Common Issues
1. **Database connection errors**: Verify DATABASE_URL
2. **Static files not loading**: Check WhiteNoise configuration
3. **Build failures**: Review Dockerfile and requirements.txt
4. **Migration errors**: Check database permissions

### Useful Commands
```bash
# View logs
docker-compose logs web

# Run shell in container
docker-compose exec web python manage.py shell

# Reset database (local only)
docker-compose down -v
docker-compose up --build
```
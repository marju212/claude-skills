# Docker Containerization

## Category
DevOps

## Description
Creating and managing Docker containers for applications. This skill covers writing Dockerfiles, building images, running containers, and managing multi-container applications with Docker Compose.

## Use Cases
- Packaging applications with all dependencies
- Creating consistent development environments
- Deploying applications across different environments
- Microservices architecture
- CI/CD pipelines

## Prerequisites
- Docker installed on your system
- Basic understanding of Linux commands
- Knowledge of your application's runtime requirements
- Familiarity with networking concepts

## Implementation

### Basic Example (Simple Node.js App)

```dockerfile
# Dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Set user to non-root
USER node

# Start application
CMD ["node", "server.js"]
```

```bash
# Build the image
docker build -t my-node-app:1.0 .

# Run the container
docker run -d -p 3000:3000 --name my-app my-node-app:1.0

# View logs
docker logs my-app

# Stop and remove
docker stop my-app
docker rm my-app
```

### Advanced Example (Multi-stage Build with Docker Compose)

```dockerfile
# Dockerfile for React + Node.js application
# Stage 1: Build frontend
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Build backend
FROM node:18-alpine AS backend-build

WORKDIR /app/backend

COPY backend/package*.json ./
RUN npm ci --only=production

COPY backend/ ./

# Stage 3: Production image
FROM node:18-alpine

WORKDIR /app

# Copy backend from build stage
COPY --from=backend-build /app/backend ./backend

# Copy frontend build from build stage
COPY --from=frontend-build /app/frontend/build ./backend/public

# Install production dependencies
WORKDIR /app/backend
RUN npm ci --only=production

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S -u 1001 -G appuser appuser

# Set ownership
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:8080/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DB_HOST=database
      - REDIS_HOST=redis
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs

  database:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

```bash
# Using Docker Compose
# Start all services
docker-compose up -d

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app

# Scale a service
docker-compose up -d --scale app=3

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Best Practices
- **Use multi-stage builds**: Reduce final image size by separating build and runtime stages
- **Minimize layers**: Combine related RUN commands to reduce image layers
- **Use specific base image tags**: Avoid `latest` tag; use specific versions for reproducibility
- **Don't run as root**: Create and use a non-root user for security
- **Use .dockerignore**: Exclude unnecessary files from build context
- **Leverage layer caching**: Order instructions from least to most frequently changed
- **Set health checks**: Enable Docker to monitor container health
- **Use environment variables**: Make containers configurable without rebuilding
- **Keep images small**: Use alpine variants and remove unnecessary dependencies
- **Scan for vulnerabilities**: Use tools like `docker scan` or Trivy

## Common Pitfalls
- **Large image sizes**: Not using multi-stage builds or including unnecessary files
- **Caching issues**: Copying files before installing dependencies breaks caching
- **Running as root**: Security risk; always create a non-root user
- **Hardcoded values**: Use environment variables or secrets for configuration
- **Not handling signals**: Application doesn't shut down gracefully
- **Missing .dockerignore**: Including node_modules, .git, etc. in build context
- **Exposing secrets**: Don't include secrets in images; use Docker secrets or env vars
- **Not considering timezone**: Be explicit about timezone if your app depends on it

## Related Skills
- [Kubernetes Deployment](./kubernetes-basics.md)
- [CI/CD Pipelines](./cicd-setup.md)
- [Container Security](./container-security.md)

## Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Play with Docker](https://labs.play-with-docker.com/)

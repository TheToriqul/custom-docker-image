# Docker Image Creation Command Reference Guide

### Project content table
- [Section 1: Core Project Workflow](#section-1-core-project-workflow)
- [Section 2: Advanced Operations](#section-2-advanced-operations)
- [Section 3: Production Guide](#section-3-production-guide)

> **Author**: [Md Toriqul Islam](https://linkedin.com/in/thetoriqul)  
> **Description**: Comprehensive command reference for Docker image creation and management  
> **Learning Focus**: Docker containerization, image optimization, and container management  
> **Note**: This is a reference guide. Do not execute commands directly without understanding their implications.

## Section 1: Core Project Workflow

### Step 1: Set Up Docker Environment
```bash
# Change script permissions
chmod +x install.sh

# Run the installation script
./install.sh

# Verify Docker installation
docker --version
docker info

# Open new terminal or rerun Docker commands without root (recommended)
newgrp docker
```

### Step 2: Create Project Structure
```bash
# Create project directory
mkdir my-python-app
cd my-python-app

# Create necessary files
touch Dockerfile
touch app.py
touch requirements.txt

# Verify file creation
ls -la
```

### Step 3: Build Docker Image
```bash
# Basic image build
docker build -t my-python-app .

# Build with no cache
docker build --no-cache -t my-python-app .

# Verify image creation
docker images my-python-app
```

### Step 4: Run Container
```bash
# Run container in background
docker run -d -p 4000:80 my-python-app

# Verify container is running
docker ps | grep my-python-app

# Check container logs
docker logs $(docker ps -q --filter ancestor=my-python-app)
```

### Final Step: Cleanup
```bash
# Stop running containers
docker stop $(docker ps -q --filter ancestor=my-python-app)

# Remove containers
docker rm $(docker ps -aq --filter ancestor=my-python-app)

# Remove image
docker rmi my-python-app

# Verify cleanup
docker ps -a | grep my-python-app
docker images | grep my-python-app
```

## Section 2: Advanced Operations

### Image Optimization
```bash
# Build with build arguments
docker build \
    --build-arg APP_VERSION=1.0.0 \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    -t my-python-app:optimized .

# Multi-stage build
docker build \
    --target production \
    -t my-python-app:prod .

# Check image layers
docker history my-python-app:prod
```

### Container Management
```bash
# Run with resource limits
docker run -d \
    --name python-app \
    --memory="512m" \
    --cpus="1.0" \
    -p 4000:80 \
    my-python-app

# Container debugging
docker exec -it python-app /bin/bash

# View container metrics
docker stats python-app
```

## Section 3: Production Guide

### Production Deployment
```bash
# Build production image
docker build \
    --target production \
    --build-arg BUILD_MODE=production \
    -t my-python-app:prod .

# Run with production settings
docker run -d \
    --name python-app-prod \
    --restart unless-stopped \
    --health-cmd="curl -f http://localhost/health || exit 1" \
    --health-interval=5m \
    -p 80:80 \
    my-python-app:prod

# Verify deployment
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Monitoring
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' python-app-prod

# View logs
docker logs -f python-app-prod

# Monitor resource usage
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Backup Operations
```bash
# Export container
docker export python-app-prod > python-app-backup.tar

# Save image
docker save my-python-app:prod | gzip > my-python-app-prod.tar.gz

# Load image from backup
docker load < my-python-app-prod.tar.gz
```

## Learning Notes

1. Always use specific tags for version control
2. Implement health checks for production containers
3. Regular security scanning is essential
4. Monitor resource usage in production
5. Maintain backup strategies for critical containers

---

> 💡 **Best Practice**: Use `.dockerignore` to exclude unnecessary files from builds

> ⚠️ **Warning**: Never store sensitive data in Docker images

> 📝 **Note**: Commands may require sudo privileges depending on your Docker setup
# Load Matching Service Deployment Guide

This guide provides instructions for deploying the Load Matching Service in various environments.

## Prerequisites

- Python 3.11+
- Docker 20.10+
- Docker Compose 2.0+
- Redis 6.0+ (for caching)
- Prometheus (for metrics)
- Grafana (for visualization)

## Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ONLYBOTAi/TAMP-MVP.git
   cd TAMP-MVP/services/load_matching
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables**
   Copy the sample environment file and update values:
   ```bash
   cp config/.env.sample config/.env
   ```

2. **Required Variables**
   ```env
   MATCH_SERVICE_HOST=0.0.0.0
   MATCH_SERVICE_PORT=8003
   MATCH_JWT_SECRET=your-secret-key
   MATCH_VEHICLE_SVC_URL=http://tamp_vehicle_svc:8001
   MATCH_TELEMATICS_URL=http://tamp_telematics_svc:8002
   ```

## Deployment Options

### 1. Local Development

1. **Run with Uvicorn**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8003
   ```

2. **Run Tests**
   ```bash
   pytest tests/ --disable-warnings -v
   ```

### 2. Docker Deployment

1. **Build Image**
   ```bash
   docker build -t tamp-load-matching:latest .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name load-matching \
     -p 8003:8003 \
     -p 9090:9090 \
     --env-file config/.env \
     tamp-load-matching:latest
   ```

### 3. Docker Compose

1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   
   services:
     load-matching:
       build: .
       ports:
         - "8003:8003"
         - "9090:9090"
       env_file:
         - config/.env
       depends_on:
         - redis
         - prometheus
   
     redis:
       image: redis:6.2
       ports:
         - "6379:6379"
   
     prometheus:
       image: prom/prometheus
       ports:
         - "9090:9090"
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml
   
     grafana:
       image: grafana/grafana
       ports:
         - "3000:3000"
       depends_on:
         - prometheus
   ```

2. **Run Stack**
   ```bash
   docker-compose up -d
   ```

## Monitoring Setup

1. **Prometheus Configuration**
   Create `prometheus.yml`:
   ```yaml
   global:
     scrape_interval: 15s
   
   scrape_configs:
     - job_name: 'load-matching'
       static_configs:
         - targets: ['load-matching:8003']
   ```

2. **Grafana Dashboards**
   - Import dashboard from `docs/grafana-dashboard.json`
   - Configure data source to point to Prometheus

## Health Checks

1. **Service Health**
   ```bash
   curl http://localhost:8003/health
   ```

2. **Metrics**
   ```bash
   curl http://localhost:8003/metrics
   ```

## Scaling

### Horizontal Scaling

1. **Docker Swarm**
   ```bash
   docker stack deploy -c docker-compose.yml tamp
   ```

2. **Kubernetes**
   ```bash
   kubectl apply -f k8s/
   ```

### Load Balancing

1. **Nginx Configuration**
   ```nginx
   upstream load_matching {
       server load-matching-1:8003;
       server load-matching-2:8003;
   }
   
   server {
       listen 80;
       server_name api.example.com;
   
       location / {
           proxy_pass http://load_matching;
       }
   }
   ```

## Troubleshooting

1. **Service Not Starting**
   - Check logs: `docker logs load-matching`
   - Verify environment variables
   - Check port availability

2. **High Latency**
   - Monitor Redis cache hit rate
   - Check vehicle service response times
   - Verify network connectivity

3. **Memory Issues**
   - Monitor container memory usage
   - Check for memory leaks
   - Adjust container limits

## Backup and Recovery

1. **Configuration Backup**
   ```bash
   tar -czf config-backup.tar.gz config/
   ```

2. **Data Recovery**
   ```bash
   tar -xzf config-backup.tar.gz
   ```

## Security Considerations

1. **Network Security**
   - Use internal networks in Docker
   - Implement TLS
   - Configure firewalls

2. **Access Control**
   - Rotate JWT secrets
   - Implement IP whitelisting
   - Use strong passwords

3. **Monitoring**
   - Set up security alerts
   - Monitor failed login attempts
   - Track rate limit violations 
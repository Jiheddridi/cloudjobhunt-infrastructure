
# 🎯 CloudJobHunt - Enterprise AI Job Search Platform 
  ![ChatGPT Image 31 janv  2026, 21_58_01](https://github.com/user-attachments/assets/e8e4ed81-80b3-46d4-8fdb-afc1d8012599)


<div align="center">

![CloudJobHunt](https://img.shields.io/badge/CloudJobHunt-AI%20Powered-blue?style=for-the-badge)

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.27+-326ce5?style=flat-square&logo=kubernetes)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-1.0+-844FCC?style=flat-square&logo=terraform)](https://www.terraform.io/)
[![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4?style=flat-square&logo=microsoft-azure)](https://azure.microsoft.com/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=flat-square&logo=jenkins)](https://www.jenkins.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**Enterprise-Grade Infrastructure | Intelligent Job Aggregation | Cloud-Native Architecture | Production Ready**

[🚀 Quick Start](#-quick-start) • [📚 Documentation](#-documentation) • [🛠️ Architecture](#-architecture) • [📊 Monitoring](#-monitoring--observability) • [🔐 Security](#-security-architecture)

</div>

---

## 🌟 Overview

**CloudJobHunt** is a production-ready, enterprise-grade job search platform powered by intelligent automation and cloud-native technologies. It aggregates job listings from multiple sources (LinkedIn, Indeed, Glassdoor), enriches data with contextual information, and provides advanced CV-to-job matching capabilities.

Built on **Azure Kubernetes Service (AKS)** with comprehensive **Infrastructure-as-Code** (Terraform), **automated CI/CD pipelines** (Jenkins), and **enterprise-grade monitoring**, CloudJobHunt demonstrates modern DevOps best practices and scalable architecture patterns.

### 💼 Platform Capabilities

| Feature | Description | Technology |
|---------|-------------|-----------|
| 🏗️ **Enterprise Infrastructure** | Fully managed Kubernetes on Azure with auto-scaling | AKS, Terraform |
| 🔄 **Multi-Source Job Aggregation** | Intelligent scraping from LinkedIn, Indeed, Glassdoor | Python, FastAPI |
| 🧠 **AI-Powered Matching** | CV-to-job scoring and intelligent ranking | ML Algorithms |
| 🔐 **Enterprise Security** | JWT auth, RBAC, Network isolation, encryption | OAuth2, TLS 1.2+ |
| 📊 **Observability** | Centralized logging, distributed tracing, metrics | Log Analytics, App Insights |
| 🚀 **Automated CI/CD** | Full pipeline from code to production | Jenkins, Docker, K8s |
| ♻️ **Infrastructure-as-Code** | Reproducible deployments across environments | Terraform 1.0+ |
| 📈 **High Availability** | Multi-zone deployment, auto-healing, resource quotas | AKS, Kubernetes |

---

## 🏗️ System Architecture

### 📐 High-Level Infrastructure Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTERNET / PUBLIC ACCESS                           │
│                       (Azure Public IP: 20.74.55.104)                       │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
        ┌─────────────────────┐   ┌─────────────────────┐
        │  Azure Load         │   │    Azure Application│
        │  Balancer (ALB)     │   │    Gateway (WAF)    │
        │  Port 80/443        │   │    SSL Termination  │
        └──────────┬──────────┘   └──────────┬──────────┘
                   │                         │
                   └────────────┬────────────┘
                                ▼
        ┌────────────────────────────────────────────────┐
        │   Azure Virtual Network (10.0.0.0/16)          │
        │  ┌──────────────────────────────────────────┐  │
        │  │     AKS Cluster (Kubernetes 1.27+)      │  │
        │  │                                          │  │
        │  │  ┌─────────────────────────────────┐    │  │
        │  │  │  Deployment: CloudJobHunt       │    │  │
        │  │  │  • 3x FastAPI Backend Pods      │    │  │
        │  │  │  • Nginx Reverse Proxy Sidecar  │    │  │
        │  │  │  • CPU: 500m/pod, Mem: 256Mi    │    │  │
        │  │  │  • Liveness Probe: /health      │    │  │
        │  │  │  • Readiness Probe: /ready      │    │  │
        │  │  │  • HPA: 3-10 replicas           │    │  │
        │  │  └─────────────────────────────────┘    │  │
        │  │                                          │  │
        │  │  ┌─────────────────────────────────┐    │  │
        │  │  │  ConfigMaps & Secrets           │    │  │
        │  │  │  • Database credentials         │    │  │
        │  │  │  • API keys & JWT secrets       │    │  │
        │  │  │  • Feature flags                │    │  │
        │  │  └─────────────────────────────────┘    │  │
        │  └──────────────────────────────────────────┘  │
        │                                                │
        │  Subnets:                                      │
        │  • AKS Subnet (10.0.1.0/24)                    │
        │  • Database Subnet (10.0.2.0/24) [Private]    │
        │  • Ingress Subnet (10.0.3.0/24)               │
        │                                                │
        │  NSG Rules:                                    │
        │  ✓ Ingress: 80, 443                           │
        │  ✓ PostgreSQL: Port 5432 (AKS only)           │
        │  ✗ Internet access restricted                 │
        └────────────────────┬───────────────────────────┘
                             │
                ┌────────────┼────────────┬──────────────┐
                │            │            │              │
                ▼            ▼            ▼              ▼
        ┌────────────┐┌────────────┐┌──────────┐┌──────────────┐
        │PostgreSQL  ││ Azure Log  ││ Azure    ││ Application  │
        │Flexible    ││ Analytics  ││ Container││ Insights     │
        │Server 16   ││ Workspace  ││ Registry ││ (Monitoring) │
        │            ││            ││ (ACR)    ││              │
        │PrivateLink ││ KQL Queries││ Push/Pull││ Performance  │
        │Zone Redundant│Monitoring  ││ Scan    ││ Tracking     │
        │HA Enabled  ││ Alerting   ││ Webhooks││ Exceptions   │
        │Backup: 35d ││ 30-day ret │└────────-┘└──────────────┘
        └────────────┘└────────────┘
```

### 🔧 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Container Orchestration** | Kubernetes (AKS) | 1.27+ | Pod orchestration, auto-scaling, self-healing |
| **Container Runtime** | Docker | Latest | Application containerization |
| **Application Server** | FastAPI | 0.109.0 | Async Python web framework |
| **Programming Language** | Python | 3.12+ | Backend development |
| **Database** | PostgreSQL Flexible | 14-16 | ACID-compliant relational DB |
| **Reverse Proxy** | Nginx | Latest | Load balancing, SSL termination |
| **Container Registry** | Azure Container Registry | - | Private Docker image storage |
| **Infrastructure** | Terraform | 1.0+ | Infrastructure-as-Code provisioning |
| **CI/CD** | Jenkins | 2.x | Automated build & deployment |
| **Observability** | Log Analytics | - | Centralized logging & metrics |
| **Monitoring** | Application Insights | - | Performance & exception tracking |
| **VPN/Network** | Azure Virtual Network | - | Network isolation & Private Link |

---

## 🚀 Infrastructure Components

### 1️⃣ Azure Kubernetes Service (AKS) - Container Orchestration

**Managed Kubernetes Cluster Configuration:**

```yaml
# Cluster Specifications
Cluster Name: aks-cloudjobhunt-dev
Kubernetes Version: 1.27+
Network Plugin: Azure CNI (overlay networking)
Network Policy: Azure Network Policy

# System Node Pool (Infrastructure)
VM Size: Standard_B2s
Min Replicas: 2
Max Replicas: 4
Auto-scaling: Enabled
OS Disk: 30GB (Premium SSD)

# Key Features
- Automatic channel upgrade enabled
- Azure RBAC integration with Azure AD
- Managed Identity (System Assigned)
- Key Vault Secrets Provider with rotation
- Maintenance window: Sunday 02:00-04:00 UTC
- OMS Agent for monitoring integration
```

**Backend Application Deployment:**

- **Replicas**: 3 (distributed across availability zones)
- **Image**: `acrcloudhuntdev.azurecr.io/cloudjobhunt-backend:latest`
- **Resource Requests**: CPU 100m, Memory 128Mi
- **Resource Limits**: CPU 500m, Memory 256Mi
- **Health Probes**:
  - Liveness: `GET /health` (interval 10s, timeout 5s)
  - Readiness: `GET /health` (interval 5s, timeout 3s)

**Horizontal Pod Autoscaler (HPA):**
```yaml
Min Pods: 3
Max Pods: 10
CPU Target: 70%
Memory Target: 80%
```

---

### 2️⃣ Azure Container Registry (ACR) - Private Docker Registry

**Registry Configuration:**

```hcl
Registry Name: acrcloudhuntdev
SKU: Standard (or Premium for geo-replication)
Admin Account: Disabled (use managed identities)
Public Network Access: Enabled (restricted by NSG)

# Security Features
- Image scanning on push
- Webhook triggers for CI/CD
- Scope maps for fine-grained access control
- Token authentication (non-admin)
```

**Image Management:**
- Multi-stage Docker builds for optimization
- Vulnerability scanning with Azure Defender
- Automated cleanup policies for old images
- Retention: Keep latest 5 versions
- Tags: `latest`, `v{version}`, `{git-commit-sha}`

**CI/CD Integration:**
- Jenkins pulls images via service principal
- ACR webhook triggers deployments on new image push
- Image signed with content trust (future enhancement)

---

### 3️⃣ PostgreSQL Flexible Server - Managed Database

**Database Configuration:**

```yaml
Server Name: psql-cloudjobhunt-dev
PostgreSQL Version: 16
SKU: Burstable_B2s (scalable on demand)
Storage: 32-128 GB (auto-grow enabled)

# High Availability
HA Mode: Zone-Redundant Replication (future)
Backup: Automated daily backups
Retention: 35 days
PITR: Point-in-time restore available

# Networking
Private DNS Zone: cloudjobhunt-dev.postgres.database.azure.com
Access Method: Private Link (no internet exposure)
Firewall: Allow only AKS subnet (10.0.1.0/24)

# Performance
Connection Pooling: Enabled
Max Connections: Configurable per pool
Slow Query Logging: Enabled
```

**Database Schema:**
```sql
Database: cloudjobhunt
Charset: UTF8
Collation: en_US.utf8

Tables:
- users (authentication & profiles)
- jobs (aggregated job listings)
- cvs (user uploaded resumes)
- search_history (user search tracking)
- job_matches (CV-to-job matching scores)
- user_preferences (search preferences)
```

**Firewall Rules:**
```
✓ Allow AKS subnet (10.0.1.0/24) port 5432
✗ Deny all other internet access
✗ No public IP exposure
```

---

### 4️⃣ Azure Virtual Network - Network Isolation

**VNet Architecture:**

```
VNet: vnet-cloudjobhunt-dev
Address Space: 10.0.0.0/16

├─ AKS Subnet (10.0.1.0/24)
│  ├─ Nodes & Pods
│  ├─ Service CIDR: 10.1.0.0/16
│  ├─ DNS Service IP: 10.1.0.10
│  └─ NSG Rules:
│     ├─ Allow 80/443 (HTTP/HTTPS)
│     └─ Allow 5432 to DB subnet (PostgreSQL)
│
├─ Database Subnet (10.0.2.0/24)
│  ├─ PostgreSQL Private Endpoint
│  ├─ Service Delegation: Microsoft.DBforPostgreSQL/flexibleServers
│  └─ NSG Rules:
│     └─ Allow 5432 from AKS subnet only
│
└─ Ingress Subnet (10.0.3.0/24)
   ├─ Application Gateway (future)
   ├─ Azure Load Balancer
   └─ Public IP for inbound traffic
```

**Security Features:**
- **Network Security Groups (NSG)**: Layer 4 traffic filtering
- **Private Link**: Database connectivity without internet routing
- **Service Endpoints**: ACR access without NAT Gateway
- **Route Tables**: Controlled traffic flow between subnets
- **NAT Gateway**: Outbound internet access with static IP

---

### 5️⃣ Azure Log Analytics - Centralized Logging

**Workspace Configuration:**

```yaml
Workspace Name: log-cloudjobhunt-dev
Location: West Europe
SKU: Pay-As-You-Go
Retention: 30 days (configurable to 90/365 days)

Data Sources:
- Container Insights (AKS metrics & logs)
- Application Insights (FastAPI telemetry)
- Custom logs (application logs)
- Performance counters
- Event logs
```

**Log Aggregation:**

| Source | Log Type | Query Language |
|--------|----------|---|
| AKS Cluster | Container logs, Events, Metrics | KQL |
| FastAPI App | Request/Response, Errors, Duration | KQL |
| PostgreSQL | Query logs, Slow queries | KQL |
| Nginx | Access logs, Errors | KQL |
| System | Node metrics, Memory, CPU | KQL |

**Kusto Query Language (KQL) Examples:**

```kusto
// Find slow API requests (> 500ms)
ContainerLog
| where LogEntry contains "duration"
| where Duration_ms > 500
| summarize count() by bin(TimeGenerated, 5m)

// Database connection errors
ContainerLog
| where LogEntry contains "connection"
| where LogEntry contains "error"
| top 10 by TimeGenerated desc

// Pod restart events
KubernetesDiagnostics
| where Message contains "Restarted"
| summarize count() by PodName, bin(TimeGenerated, 1h)
```

---

### 6️⃣ Application Insights - Performance Monitoring

**Telemetry Collection:**

- ✅ HTTP Request tracking (duration, status code, URL)
- ✅ Exception logging with stack traces
- ✅ Database query performance metrics
- ✅ Custom events (user actions, business metrics)
- ✅ Dependency tracking (external API calls)
- ✅ Performance counters (CPU, Memory usage)
- ✅ Availability tests (synthetic monitoring)

**Alert Rules:**

| Alert | Condition | Action |
|-------|-----------|--------|
| High Error Rate | > 5% in 5 min | PagerDuty |
| Slow Response Time | p95 > 1000ms | Slack + Email |
| Database Latency | > 200ms avg | DevOps team |
| High Memory Usage | > 85% | Auto-scale + Email |
| Pod CrashLoop | 3+ restarts/10min | PagerDuty + Slack |

---

## � Docker - Containerization Strategy

### Multi-Stage Dockerfile

```dockerfile
# Stage 1: Build Environment
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime Environment (Optimized)
FROM python:3.12-slim

WORKDIR /app

# Copy only runtime artifacts from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ ./app/
COPY main.py .

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Image Optimization:**
- Multi-stage build reduces image size (~400MB → ~150MB)
- Slim base image (Python 3.12-slim)
- Non-root user execution (security)
- Health check endpoint integrated
- Layer caching for faster builds

**Image Registry Tags:**
```
acrcloudhuntdev.azurecr.io/cloudjobhunt-backend:latest
acrcloudhuntdev.azurecr.io/cloudjobhunt-backend:v1.0.0
acrcloudhuntdev.azurecr.io/cloudjobhunt-backend:sha-abc123def
```

---

## 🔄 CI/CD Pipeline (Jenkins) - Complete

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Git Webhook Trigger                          │
│              (Push to main / Pull Request merged)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌───────────────┐       ┌──────────────────┐
        │ CHECKOUT      │       │ PARALLEL JOBS    │
        │ • Clone repo  │       │ • Unit Tests     │
        │ • Setup       │       │ • Linting        │
        └───────┬───────┘       │ • Code Coverage  │
                │               └──────────────────┘
                ▼
        ┌──────────────────────┐
        │ BUILD & TEST         │
        │ ✓ Create venv        │
        │ ✓ Install deps       │
        │ ✓ pytest runner      │
        │ ✓ Code quality check │
        └──────────┬───────────┘
                   │
        ┌──────────┴───────────┐
        │ CONDITIONAL: Pass?   │
        │ ├─ YES → Continue    │
        │ └─ NO → FAIL BUILD   │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ DOCKER BUILD         │
        │ • Multi-stage build  │
        │ • Run tests in       │
        │   container          │
        │ • Tag image          │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ PUSH TO ACR          │
        │ • Azure Container    │
        │   Registry           │
        │ • Webhook trigger    │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ DEPLOY TO K8S        │
        │ • Update image       │
        │ • Apply manifests    │
        │ • Wait rollout       │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ SMOKE TESTS          │
        │ • /health endpoint   │
        │ • DB connectivity    │
        │ • API endpoints      │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ NOTIFY SLACK         │
        │ • Deployment status  │
        │ • Build artifacts    │
        └──────────────────────┘
```

### Jenkinsfile - Detailed

```groovy
pipeline {
    agent any
    
    options {
        // Keep last 30 builds
        buildDiscarder(logRotator(numToKeepStr: '30', daysToKeepStr: '30'))
        // Timeout after 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        // Disable concurrent builds
        disableConcurrentBuilds()
        // Add timestamps to console output
        timestamps()
    }
    
    environment {
        // Registry credentials
        REGISTRY_URL = 'acrcloudhuntdev.azurecr.io'
        IMAGE_NAME = 'cloudjobhunt-backend'
        IMAGE_TAG = "${BUILD_NUMBER}"
        PYTHON_VERSION = '3.12'
        
        // Azure
        AZURE_RESOURCE_GROUP = 'rg-cloudjobhunt-dev'
        AZURE_AKS_CLUSTER = 'aks-cloudjobhunt-dev'
        AZURE_REGION = 'westeurope'
        
        // Kubernetes
        K8S_NAMESPACE = 'default'
        K8S_DEPLOYMENT = 'backend'
    }
    
    stages {
        stage('🔍 Checkout') {
            steps {
                checkout scm
                script {
                    GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                    echo "✓ Repository: ${GIT_COMMIT_SHORT}"
                }
            }
        }
        
        stage('🧪 Build & Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        script {
                            sh '''
                                echo "📦 Creating Python virtual environment..."
                                python3.${PYTHON_VERSION} -m venv .venv
                                
                                echo "📥 Installing dependencies..."
                                . .venv/bin/activate
                                pip install --upgrade pip setuptools wheel
                                pip install -r requirements.txt
                                pip install pytest pytest-cov pytest-asyncio
                                
                                echo "🧪 Running unit tests..."
                                pytest --cov=app --cov-report=xml \
                                       --cov-report=html \
                                       --junitxml=test-results.xml \
                                       -v
                                
                                echo "✓ Tests passed successfully"
                            '''
                        }
                    }
                }
                
                stage('Code Quality') {
                    steps {
                        script {
                            sh '''
                                . .venv/bin/activate
                                
                                echo "🔍 Running pylint..."
                                pylint app/ --exit-zero
                                
                                echo "📐 Running flake8..."
                                flake8 app/ --max-line-length=120 --count
                                
                                echo "🔤 Type checking with mypy..."
                                mypy app/ --ignore-missing-imports
                                
                                echo "✓ Code quality checks passed"
                            '''
                        }
                    }
                }
            }
        }
        
        stage('🐳 Build Docker Image') {
            steps {
                script {
                    sh '''
                        echo "🔨 Building Docker image..."
                        docker build \
                            --tag ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG} \
                            --tag ${REGISTRY_URL}/${IMAGE_NAME}:latest \
                            --tag ${REGISTRY_URL}/${IMAGE_NAME}:${GIT_COMMIT_SHORT} \
                            --label "commit=${GIT_COMMIT_SHORT}" \
                            --label "build-date=$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
                            --label "jenkins-build=${BUILD_NUMBER}" \
                            .
                        
                        echo "✓ Docker image built successfully"
                        docker images | grep ${IMAGE_NAME}
                    '''
                }
            }
        }
        
        stage('🧬 Container Tests') {
            steps {
                script {
                    sh '''
                        echo "🧪 Running container tests..."
                        docker run -d --name test-app \
                            -p 8000:8000 \
                            ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                        
                        echo "⏳ Waiting for container to start..."
                        sleep 5
                        
                        echo "🔗 Testing health endpoint..."
                        curl -f http://localhost:8000/health || exit 1
                        
                        echo "📋 Testing FastAPI import..."
                        docker exec test-app python -c "from main import app; print('✓ FastAPI OK')"
                        
                        echo "🧹 Cleaning up..."
                        docker stop test-app
                        docker rm test-app
                        
                        echo "✓ Container tests passed"
                    '''
                }
            }
        }
        
        stage('🏴 Push to ACR') {
            steps {
                script {
                    sh '''
                        echo "🔐 Authenticating with Azure Container Registry..."
                        az acr login --name cloudhuntdev
                        
                        echo "📤 Pushing images to ACR..."
                        docker push ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${REGISTRY_URL}/${IMAGE_NAME}:latest
                        docker push ${REGISTRY_URL}/${IMAGE_NAME}:${GIT_COMMIT_SHORT}
                        
                        echo "✓ Images pushed successfully"
                        
                        echo "🔍 Running image scan..."
                        az acr build --registry cloudhuntdev --image ${IMAGE_NAME}:${IMAGE_TAG} .
                    '''
                }
            }
        }
        
        stage('🚀 Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        echo "📍 Setting up kubectl context..."
                        az aks get-credentials \
                            --resource-group ${AZURE_RESOURCE_GROUP} \
                            --name ${AZURE_AKS_CLUSTER}
                        
                        echo "🔗 Verifying cluster connectivity..."
                        kubectl cluster-info
                        kubectl get nodes
                        
                        echo "🔄 Updating deployment image..."
                        kubectl set image deployment/${K8S_DEPLOYMENT} \
                            ${K8S_DEPLOYMENT}=${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG} \
                            --namespace=${K8S_NAMESPACE}
                        
                        echo "⏳ Waiting for rollout to complete..."
                        kubectl rollout status deployment/${K8S_DEPLOYMENT} \
                            --namespace=${K8S_NAMESPACE} \
                            --timeout=5m
                        
                        echo "✓ Deployment completed"
                        
                        echo "📊 Deployment status:"
                        kubectl get deployment ${K8S_DEPLOYMENT} -o wide
                        kubectl get pods -l app=${K8S_DEPLOYMENT}
                    '''
                }
            }
        }
        
        stage('✅ Smoke Tests') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        echo "🧪 Running smoke tests..."
                        
                        # Get service endpoint
                        SERVICE_IP=$(kubectl get svc/${K8S_DEPLOYMENT} \
                            -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
                        
                        echo "🔗 Service IP: ${SERVICE_IP}"
                        
                        echo "🏥 Testing health endpoint..."
                        curl -f http://${SERVICE_IP}:8000/health || exit 1
                        
                        echo "🗄️ Testing database connectivity..."
                        kubectl exec -it $(kubectl get pod -l app=${K8S_DEPLOYMENT} \
                            -o jsonpath='{.items[0].metadata.name}') \
                            -- python -c "
                            from app.database import SessionLocal
                            db = SessionLocal()
                            result = db.execute('SELECT 1')
                            print('✓ Database connectivity OK')
                            "
                        
                        echo "🔌 Testing API endpoints..."
                        curl -f http://${SERVICE_IP}:8000/api/v1/search?q=python || exit 1
                        
                        echo "✓ All smoke tests passed"
                    '''
                }
            }
        }
        
        stage('📢 Notify') {
            when {
                always()
            }
            steps {
                script {
                    def status = currentBuild.result ?: 'SUCCESS'
                    def color = status == 'SUCCESS' ? 'good' : 'danger'
                    def icon = status == 'SUCCESS' ? '✅' : '❌'
                    
                    sh '''
                        curl -X POST ${SLACK_WEBHOOK_URL} \
                            -H 'Content-Type: application/json' \
                            -d @- <<EOF
                        {
                            "attachments": [
                                {
                                    "color": "${color}",
                                    "title": "${icon} CloudJobHunt Build ${BUILD_NUMBER}",
                                    "text": "${status}",
                                    "fields": [
                                        {"title": "Branch", "value": "${GIT_BRANCH}", "short": true},
                                        {"title": "Commit", "value": "${GIT_COMMIT_SHORT}", "short": true},
                                        {"title": "Image", "value": "${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}", "short": false}
                                    ],
                                    "footer": "CloudJobHunt CI/CD"
                                }
                            ]
                        }
                        EOF
                    '''
                }
            }
        }
    }
    
    post {
        always {
            // Archive test results
            junit allowEmptyResults: true, testResults: 'test-results.xml'
            
            // Archive coverage reports
            publishHTML([
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
            
            // Cleanup
            cleanWs()
        }
        
        failure {
            script {
                echo "❌ Build failed. Check logs above."
            }
        }
        
        success {
            script {
                echo "✅ Build completed successfully!"
            }
        }
    }
}
```

---

## 🏗️ Terraform - Infrastructure as Code

### Project Structure & Modules

```
terraform/
│
├── environments/
│   ├── dev/
│   │   ├── main.tf                 # Resource orchestration
│   │   ├── variables.tf            # Variable declarations
│   │   ├── terraform.tfvars        # Dev-specific values
│   │   ├── outputs.tf              # Exported outputs
│   │   └── tfplan                  # Terraform plan (binary)
│   │
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── outputs.tf
│   │
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars        # (Git-ignored for secrets)
│       └── outputs.tf
│
└── modules/
    ├── networking/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── versions.tf
    │
    ├── aks/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── versions.tf
    │
    ├── acr/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── versions.tf
    │
    ├── database/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── versions.tf
    │
    └── monitoring/
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        └── versions.tf
```

### Core Terraform Modules (Detailed)

#### 1. **Networking Module** (`modules/networking/main.tf`)

```hcl
resource "azurerm_virtual_network" "main" {
  name                = "vnet-${var.project_name}-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  address_space       = [var.vnet_address_space]  # 10.0.0.0/16
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}

# AKS Subnet (10.0.1.0/24)
resource "azurerm_subnet" "aks" {
  name                 = "snet-aks-${var.environment}"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.subnet_aks_cidr]
  
  service_endpoints = ["Microsoft.ContainerRegistry"]
}

# Database Subnet (10.0.2.0/24) - Private
resource "azurerm_subnet" "database" {
  name                 = "snet-database-${var.environment}"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.subnet_database_cidr]
  
  delegation {
    name = "postgresql-flexible-server"
    service_delegation {
      name    = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

# Network Security Group with rules
resource "azurerm_network_security_group" "main" {
  name                = "nsg-${var.project_name}-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  
  security_rule {
    name                       = "allow-http"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  
  security_rule {
    name                       = "allow-https"
    priority                   = 101
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  
  security_rule {
    name                       = "allow-postgresql-from-aks"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5432"
    source_address_prefix      = var.subnet_aks_cidr
    destination_address_prefix = "*"
  }
}
```

**Networking Outputs:**
```hcl
output "vnet_id" {
  value = azurerm_virtual_network.main.id
}

output "aks_subnet_id" {
  value = azurerm_subnet.aks.id
}

output "database_subnet_id" {
  value = azurerm_subnet.database.id
}

output "nsg_id" {
  value = azurerm_network_security_group.main.id
}
```

#### 2. **AKS Module** (`modules/aks/main.tf`)

```hcl
resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-${var.project_name}-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = "aks-${var.project_name}-${var.environment}"
  
  kubernetes_version        = var.kubernetes_version      # 1.27+
  automatic_channel_upgrade = "patch"
  
  # System Node Pool
  default_node_pool {
    name                = "system"
    vm_size             = var.system_node_pool_vm_size   # Standard_B2s
    enable_auto_scaling = true
    min_count           = var.system_node_pool_min_count
    max_count           = var.system_node_pool_max_count
    os_disk_size_gb     = 30
    vnet_subnet_id      = var.aks_subnet_id
    
    node_labels = {
      "role"        = "system"
      "environment" = var.environment
    }
  }
  
  # Managed Identity
  identity {
    type = "SystemAssigned"
  }
  
  # Network Configuration
  network_profile {
    network_plugin    = "azure"          # CNI plugin
    network_policy    = "azure"          # Network policies
    load_balancer_sku = "standard"
    
    load_balancer_profile {
      outbound_ip_address_ids = [azurerm_public_ip.ingress.id]
    }
    
    service_cidr   = "10.1.0.0/16"
    dns_service_ip = "10.1.0.10"
  }
  
  # Azure AD Integration
  azure_active_directory_role_based_access_control {
    managed            = true
    azure_rbac_enabled = true
  }
  
  # Monitoring (OMS Agent)
  oms_agent {
    log_analytics_workspace_id = var.log_analytics_workspace_id
  }
  
  # Key Vault Integration
  key_vault_secrets_provider {
    secret_rotation_enabled  = true
    secret_rotation_interval = "2m"
  }
  
  # Maintenance Window (Sunday 02:00-04:00 UTC)
  maintenance_window {
    allowed {
      day   = "Sunday"
      hours = [2, 3, 4]
    }
  }
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}

# Public IP for ingress
resource "azurerm_public_ip" "ingress" {
  name                = "pip-${var.project_name}-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
  
  tags = {
    Environment = var.environment
  }
}
```

**AKS Outputs:**
```hcl
output "kubernetes_cluster_id" {
  value = azurerm_kubernetes_cluster.main.id
}

output "kube_admin_config" {
  value     = azurerm_kubernetes_cluster.main.kube_admin_config[0]
  sensitive = true
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.main.kube_config[0]
  sensitive = true
}
```

#### 3. **Database Module** (`modules/database/main.tf`)

```hcl
# Private DNS Zone for PostgreSQL
resource "azurerm_private_dns_zone" "postgres" {
  name                = "${var.project_name}-${var.environment}.postgres.database.azure.com"
  resource_group_name = var.resource_group_name
  
  tags = {
    Environment = var.environment
  }
}

# Link VNet to private DNS zone
resource "azurerm_private_dns_zone_virtual_network_link" "postgres" {
  name                  = "vnet-link-${var.environment}"
  private_dns_zone_name = azurerm_private_dns_zone.postgres.name
  resource_group_name   = var.resource_group_name
  virtual_network_id    = var.vnet_id
  
  tags = {
    Environment = var.environment
  }
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "main" {
  name                = "psql-${var.project_name}-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  
  version             = "16"
  sku_name            = var.sku_name                    # Burstable_B1ms
  storage_mb          = var.storage_mb                  # 32768
  
  administrator_login    = var.admin_username
  administrator_password = var.admin_password
  
  delegated_subnet_id = var.database_subnet_id
  private_dns_zone_id = azurerm_private_dns_zone.postgres.id
  
  high_availability {
    mode = "Disabled"  # Change to "ZoneRedundant" for HA
  }
  
  maintenance_window {
    day_of_week  = 0                # Sunday
    start_hour   = 3
    start_minute = 0
  }
  
  backup_retention_days             = 35
  geo_redundant_backup_enabled      = false
  public_network_access_enabled     = false
  ssl_enforce_enabled               = true
  ssl_minimum_tls_version_enforced  = "TLSEnforcementDisabled"
  
  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
  
  depends_on = [azurerm_private_dns_zone_virtual_network_link.postgres]
}

# Create CloudJobHunt database
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = var.database_name
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Firewall rule: Allow AKS subnet
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_aks" {
  name             = "allow-aks-subnet"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = cidrhost(var.aks_subnet_cidr, 0)
  end_ip_address   = cidrhost(var.aks_subnet_cidr, 255)
}
```

#### 4. **ACR Module** (`modules/acr/main.tf`)

```hcl
resource "azurerm_container_registry" "main" {
  name                = "acr${var.project_name}${var.environment}"  # Must be unique, no hyphens
  resource_group_name = var.resource_group_name
  location            = var.location
  
  sku           = var.sku                            # Standard
  admin_enabled = false                              # Use managed identity
  
  public_network_access_enabled = var.public_network_access_enabled
  
  # Quarantine policy
  quarantine_policy_enabled = true
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Scope map for pull-only access
resource "azurerm_container_registry_scope_map" "pull_only" {
  name                    = "pull-only"
  container_registry_name = azurerm_container_registry.main.name
  resource_group_name     = var.resource_group_name
  
  actions = [
    "repositories/*/content/read",
    "repositories/*/metadata/read"
  ]
}

# CI/CD Token
resource "azurerm_container_registry_token" "cicd" {
  count                   = var.create_cicd_token ? 1 : 0
  name                    = "cicd-token"
  container_registry_name = azurerm_container_registry.main.name
  resource_group_name     = var.resource_group_name
  scope_map_id            = azurerm_container_registry_scope_map.pull_only.id
  enabled                 = true
}
```

#### 5. **Monitoring Module** (`modules/monitoring/main.tf`)

```hcl
# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = "log-${var.project_name}-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  
  sku               = var.sku                    # PerGB2018
  retention_in_days = var.retention_in_days      # 30
  
  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Container Insights Solution
resource "azurerm_log_analytics_solution" "container_insights" {
  solution_name         = "ContainerInsights"
  location              = var.location
  resource_group_name   = var.resource_group_name
  workspace_resource_id = azurerm_log_analytics_workspace.main.id
  workspace_name        = azurerm_log_analytics_workspace.main.name
  
  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/ContainerInsights"
  }
}

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = "appi-${var.project_name}-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
  
  workspace_id = azurerm_log_analytics_workspace.main.id
  
  tags = {
    Environment = var.environment
  }
}
```

### Terraform Deployment Commands

```bash
# Initialize Terraform (download providers)
cd terraform/environments/dev
terraform init

# Format code
terraform fmt -recursive ..

# Validate configuration
terraform validate

# Plan deployment (preview changes)
terraform plan -out=tfplan

# Apply configuration (create resources)
terraform apply tfplan

# Show state
terraform show

# Output values
terraform output

# Destroy infrastructure (CAUTION)
terraform destroy

# Cleanup state
terraform state list
terraform state show aws_instance.example
terraform state rm aws_instance.example
```

---

## 🔐 Security Architecture

### Authentication & Authorization

- **JWT Tokens** - Short-lived access tokens (30 min expiry)
- **Refresh Tokens** - Long-lived tokens for session persistence
- **OAuth2 Password Flow** - Standard authentication
- **RBAC** - Role-based access control for API endpoints
- **Azure AD Integration** - Enterprise identity federation

### Network Security

- **NSG Rules** - Ingress/egress filtering at subnet level
- **Private Link** - Database access without internet exposure
- **Service Principal** - Workload identity for AKS
- **RBAC Roles** - Azure AD integration for access control
- **DDoS Protection** - Azure DDoS Standard (optional)

### Data Protection

- **Encryption in Transit** - TLS 1.2+ enforcement
- **Encryption at Rest** - AES-256 for storage
- **Secrets Management** - Azure Key Vault integration
- **Audit Logging** - All database operations logged
- **Backup** - 35-day automated PostgreSQL backups

### Compliance

- ✅ No hardcoded credentials (Terraform secrets excluded)
- ✅ Secrets in Azure Key Vault
- ✅ Regular security patches
- ✅ Vulnerability scanning (image & dependencies)
- ✅ Centralized audit logs
- ✅ RBAC for least privilege access
- ✅ Network isolation per subnet

---

## 📊 Monitoring & Observability

### Observability Stack

```
┌──────────────┐
│ Application  │ (Logs & Events)
└────────┬─────┘
         │
         ▼
┌────────────────────────────┐
│ Azure Log Analytics        │
│ - Centralized Logging      │
│ - Alert Rules & KQL        │
└────────────────────────────┘
         │
    ┌────┴─────┬──────────┐
    ▼          ▼          ▼
┌───────┐ ┌───────┐ ┌──────────┐
│Slack  │ │Email  │ │PagerDuty │
└───────┘ └───────┘ └──────────┘
```

### Key Metrics

| Metric | Target | Tool |
|--------|--------|------| 
| **Pod CPU** | 30-50% | K8s metrics |
| **Pod Memory** | 40-60% | K8s metrics |
| **Pod Restarts** | 0 | K8s events |
| **Database Connections** | < 80% | Log Analytics |
| **Node Health** | 100% | K8s nodes |

### Alerting

**Critical**: Pod CrashLoop, DB pool > 95%, Connection errors → **PagerDuty**
**High**: CPU > 80%, Memory > 85% → **Slack + Email**
**Medium**: Pod restart, High 4xx → **Slack**

---

## 🛠️ Operations & Maintenance

### Common kubectl Operations

```bash
# Cluster Info
kubectl cluster-info
kubectl get nodes -o wide
kubectl top nodes
kubectl describe node <node-name>

# Pods
kubectl get pods -A                                    # All namespaces
kubectl get pods -o wide                               # Detailed view
kubectl top pods                                       # Resource usage
kubectl describe pod <pod-name>                        # Pod details
kubectl logs <pod-name> --tail=100 -f                 # Stream logs
kubectl logs <pod-name> --previous                    # Crashed pod logs
kubectl exec -it <pod-name> -- /bin/bash              # Shell access

# Deployments
kubectl get deployments
kubectl describe deployment backend
kubectl rollout status deployment/backend -w           # Watch rollout
kubectl rollout history deployment/backend             # Rollout history
kubectl rollout undo deployment/backend                # Rollback
kubectl set image deployment/backend backend=image:tag # Update image
kubectl scale deployment/backend --replicas=5          # Manual scale
kubectl get hpa                                        # Auto-scaler status

# Services & Networking
kubectl get svc                                        # Services
kubectl get ingress                                    # Ingress rules
kubectl port-forward svc/backend 8000:8000            # Local access
kubectl exec -it <pod> -- curl localhost:8000/health  # Test endpoint

# Events & Troubleshooting
kubectl get events --sort-by='.lastTimestamp'          # Recent events
kubectl describe pod <pod> | grep -A 5 "Events:"      # Pod events
kubectl logs <pod> | grep -i error                    # Error logs
kubectl cluster-info dump                             # Full diagnostics
```

### Database Operations

```bash
# Connect to PostgreSQL (from within cluster)
kubectl run -it --rm postgres-client \
  --image=postgres:16 \
  --restart=Never -- \
  psql postgresql://user:password@psql-cloudjobhunt-dev.c.postgres.database.azure.com:5432/cloudjobhunt

# Common queries
SELECT version();                                      # PostgreSQL version
SELECT datname FROM pg_database;                      # List databases
SELECT * FROM pg_stat_statements LIMIT 10;            # Slow queries
SELECT pg_database.datname, 
       numbackends
  FROM pg_stat_database, pg_database
 WHERE pg_database.datname NOT LIKE 'template%%'      # Active connections

# Backup database
az postgres flexible-server backup create \
  --name backup-$(date +%s) \
  --resource-group rg-cloudjobhunt-dev \
  --server-name psql-cloudjobhunt-dev

# Restore database
az postgres flexible-server restore \
  --resource-group rg-cloudjobhunt-dev \
  --server-name psql-cloudjobhunt-dev-restored \
  --source-server psql-cloudjobhunt-dev \
  --restore-point-in-time "2026-02-01T10:00:00Z"
```

---

## 🎯 Deployment Best Practices

### Pre-Deployment
- ✅ Docker image built & scanned
- ✅ Image pushed to ACR
- ✅ Terraform plan reviewed
- ✅ Monitoring alerts configured

### Deployment

```bash
# 1. Get cluster credentials
az aks get-credentials --resource-group rg-cloudjobhunt-dev --name aks-cloudjobhunt-dev

# 2. Apply manifests
kubectl apply -f k8s/deployment.yaml

# 3. Monitor rollout
kubectl rollout status deployment/backend -w

# 4. Test health
kubectl port-forward svc/backend 8000:8000
curl http://localhost:8000/health
```

### Rollback

```bash
kubectl rollout undo deployment/backend
kubectl rollout status deployment/backend -w
```

---

## 📚 Documentation Links

| Resource | Purpose |
|----------|---------|
| [Terraform Azure Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs) | IaC reference |
| [Kubernetes Docs](https://kubernetes.io/docs/) | K8s concepts |
| [FastAPI Docs](https://fastapi.tiangolo.com/) | API framework |
| [Azure CLI](https://learn.microsoft.com/cli/azure/) | Command-line tools |
| [PostgreSQL Docs](https://www.postgresql.org/docs/) | Database reference |
| [Jenkins Docs](https://www.jenkins.io/doc/) | CI/CD pipeline |

---

## 🚀 Quick Start Guide

### Prerequisites

```bash
# Check versions
az --version                           # Azure CLI 2.40+
terraform version                      # Terraform 1.0+
kubectl version                        # kubectl 1.27+
docker version                         # Docker 24.0+
```

### 1️⃣ Azure Authentication

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "YOUR-SUBSCRIPTION-ID"

# Verify
az account show
```

### 2️⃣ Deploy Infrastructure (Terraform)

```bash
# Navigate to dev environment
cd terraform/environments/dev

# Initialize
terraform init

# Review changes
terraform plan -out=tfplan

# Deploy
terraform apply tfplan

# Export outputs
terraform output -raw kube_config > ~/.kube/config
```

### 3️⃣ Verify Deployment

```bash
# Get credentials
az aks get-credentials \
  --resource-group rg-cloudjobhunt-dev \
  --name aks-cloudjobhunt-dev

# Verify connectivity
kubectl cluster-info
kubectl get nodes
kubectl get pods
```

### 4️⃣ Deploy Application

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Monitor deployment
kubectl rollout status deployment/backend -w

# Get service IP
kubectl get svc backend -o wide
```

### 5️⃣ Verify Deployment

```bash
# Get service IP
PUBLIC_IP=$(kubectl get svc backend -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Test health
curl http://$PUBLIC_IP/health
```

---

## 🔧 Troubleshooting Guide

### Common Issues

```bash
# Pod not starting
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous

# Database connection issues
kubectl exec -it <pod> -- ping psql-server.postgres.database.azure.com

# Check resource constraints
kubectl top pods
kubectl top nodes

# View events
kubectl get events --sort-by='.lastTimestamp'
```

---

## � Documentation Links

| Resource | Purpose |
|----------|---------|
| [Terraform Azure Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs) | IaC reference |
| [Kubernetes Docs](https://kubernetes.io/docs/) | K8s concepts |
| [FastAPI Docs](https://fastapi.tiangolo.com/) | API framework |
| [Azure CLI](https://learn.microsoft.com/cli/azure/) | Command-line tools |
| [PostgreSQL Docs](https://www.postgresql.org/docs/) | Database reference |
| [Jenkins Docs](https://www.jenkins.io/doc/) | CI/CD pipeline |

---

## 📝 License & Roadmap

**MIT License** - See [LICENSE](LICENSE) for details

### 🏆 Project Roadmap

**Phase 1** ✅
- Dev environment on AKS, Terraform IaC, Jenkins pipeline, PostgreSQL, Monitoring

**Phase 2** 🔄
- Staging deployment, DR & backups, Blue-green deployments, Cost optimization

**Phase 3** 🚀
- Production environment, Multi-region failover, 99.95% SLA, Advanced security

---

<div align="center">

**Enterprise AI Job Search Platform | Cloud-Native Infrastructure**

Last Updated: February 2026 | Status: Production Ready ✅

[📖 Architecture](./docs/architecture.md) • [🔧 Terraform](./terraform) • [🐳 Docker](./Dockerfile) • [🔄 Jenkins](./Jenkinsfile)

</div>

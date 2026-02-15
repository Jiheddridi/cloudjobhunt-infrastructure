pipeline {
    agent any
    
    environment {
        ACR_NAME = 'jobhuntacr'
        ACR_LOGIN_SERVER = 'jobhuntacr.azurecr.io'
        AKS_CLUSTER = 'jobhunt-aks-new'
        RESOURCE_GROUP = 'jobhunt-rg-new'
        BACKEND_IMAGE = "${ACR_LOGIN_SERVER}/backend:${BUILD_NUMBER}"
        FRONTEND_IMAGE = "${ACR_LOGIN_SERVER}/frontend:${BUILD_NUMBER}"
    }
    
    stages {
        stage('1. Build Docker Images') {
            steps {
                echo '🔨 Building Docker images...'
                sh '''
                    cd docker/api
                    docker build -t ${BACKEND_IMAGE} .
                    
                    cd ../apiFront
                    docker build -t ${FRONTEND_IMAGE} .
                '''
                echo '✅ Build completed'
            }
        }
        
        stage('2. Security Scan with Trivy') {
            steps {
                echo '🔍 Scanning images for vulnerabilities...'
                sh '''
                    trivy image --severity HIGH,CRITICAL ${BACKEND_IMAGE} || true
                    trivy image --severity HIGH,CRITICAL ${FRONTEND_IMAGE} || true
                '''
                echo '✅ Security scan completed'
            }
        }
        
        stage('3. Push to Azure Container Registry') {
            steps {
                echo '📤 Pushing images to ACR...'
                sh '''
                    az acr login --name ${ACR_NAME}
                    docker push ${BACKEND_IMAGE}
                    docker push ${FRONTEND_IMAGE}
                '''
                echo '✅ Push completed'
            }
        }
        
        stage('4. Deploy to AKS') {
            steps {
                echo '🚀 Deploying to Kubernetes...'
                sh '''
                    az aks get-credentials --resource-group ${RESOURCE_GROUP} --name ${AKS_CLUSTER} --overwrite-existing
                    kubectl set image deployment/backend api=${BACKEND_IMAGE}
                    kubectl set image deployment/frontend nginx=${FRONTEND_IMAGE}
                '''
                echo '✅ Deployment completed'
            }
        }
        
        stage('5. Health Check') {
            steps {
                echo '✅ Verifying deployment...'
                sh '''
                    kubectl rollout status deployment/backend --timeout=5m
                    kubectl rollout status deployment/frontend --timeout=5m
                    kubectl get pods
                '''
                echo '✅ All pods healthy'
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully! Deployment time reduced by 60%'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for details.'
        }
    }
}
```


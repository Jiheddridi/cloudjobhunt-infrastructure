pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                // Créer un environnement virtuel
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip'
                sh '. .venv/bin/activate && pip install -r requirements.txt'

                // Tester l'import FastAPI
                sh '. .venv/bin/activate && python -c "from main import app; print(\\"✅ FastAPI loaded OK\\")"'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t cloudjobhunt-backend:latest .'
            }
        }

        stage('Run Container (Test)') {
            steps {
                sh '''
                    docker run -d --name test-app -p 8000:8000 cloudjobhunt-backend:latest
                    sleep 5
                    curl -f http://localhost:8000/health || exit 1
                    docker stop test-app
                    docker rm test-app
                '''
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
            cleanWs()
        }
    }
}

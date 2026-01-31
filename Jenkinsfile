pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test in Subdirectory') {
            steps {
                dir('cloudjobhunt-infrastructure') {
                    // Créer un environnement virtuel
                    sh 'python3 -m venv .venv'
                    sh '. .venv/bin/activate && pip install --upgrade pip'
                    sh '. .venv/bin/activate && pip install -r requirements.txt'

                    // Tester l'import de l'application
                    sh '. .venv/bin/activate && python -c "from main import app; print(\"✅ FastAPI app loaded OK\")"'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('cloudjobhunt-infrastructure') {
                    sh 'docker build -t cloudjobhunt-backend:latest .'
                }
            }
        }

        stage('Run Container (Test)') {
            steps {
                dir('cloudjobhunt-infrastructure') {
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
    }

    post {
        always {
            sh 'docker system prune -f'
            cleanWs()
        }
    }
}

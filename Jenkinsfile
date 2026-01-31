pipeline {
    agent any

    environment {
        APP_NAME = "cloudjobhunt-backend"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test in Subdirectory') {
            steps {
                dir('cloudjobhunt-infrastructure') {
                    // Vérifier Python
                    sh 'python3 --version'
                    sh 'pip3 install --upgrade pip'

                    // Installer dépendances
                    sh 'pip3 install -r requirements.txt'

                    // Test de santé rapide (simule un test)
                    sh 'python3 -c "from main import app; print(\"✅ FastAPI app imported OK\")"'

                    // Optionnel : ajouter un vrai test avec pytest plus tard
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('cloudjobhunt-infrastructure') {
                    sh 'docker build -t ${APP_NAME}:${IMAGE_TAG} .'
                    sh 'docker images | grep ${APP_NAME}'
                }
            }
        }

        stage('Run Container (Test)') {
            steps {
                dir('cloudjobhunt-infrastructure') {
                    // Lancer temporairement le conteneur et vérifier qu'il répond
                    sh '''
                        docker run -d --name test-app -p 8000:8000 ${APP_NAME}:${IMAGE_TAG}
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
            sh 'docker system prune -f'  // Nettoie les images/conteneurs temporaires
            cleanWs()
        }
    }
}

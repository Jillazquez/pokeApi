pipeline {
    agent any 
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app:latest' 
        CONTAINER_NAME = 'pokeapi-container' 
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Jillazquez/pokeApi.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t $DOCKER_IMAGE .'  
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    echo 'Running Docker Compose...'
                    sh 'docker-compose up -d'  
                }
            }
        }


        stage('Run Pytest') {
            steps {
                script {
                    echo 'Running Pytest...'
                    sh 'docker exec pokeapi-container /app/venv/bin/pytest tests/'  
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'  
        }
        failure {
            echo 'There was an issue with the pipeline.'
        }
    }
}

pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t pokeapi-app .'
                }
            }
        }
        
        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker run -d -p 8000:8000 --name pokeapi-container pokeapi-app || true'
                }
            }
        }
        
        stage('Test Application') {
            steps {
                script {
                    sh 'curl -f http://localhost:8000 || exit 1'
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    sh '''
                        docker stop pokeapi-container || true
                        docker rm pokeapi-container || true
                        docker rmi pokeapi-app || true
                    '''
                }
            }
        }
    }
}

pipeline {
    agent any  // Utiliza cualquier nodo de Jenkins disponible
    
    environment {
        DOCKER_IMAGE = 'pokeapi:latest'  // Define el nombre de la imagen Docker
        CONTAINER_NAME = 'pokeapi_container'  // Nombre del contenedor para referencia
    }

    stages {
        stage('Checkout') {
            steps {
                // Realiza el checkout del repositorio de GitHub
                git url: 'https://github.com/Jillazquez/pokeApi.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Construir la imagen Docker
                    echo 'Building Docker image...'
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Ejecutar el contenedor Docker en segundo plano
                    echo 'Running Docker container...'
                    sh 'docker run -d --name $CONTAINER_NAME -p 8000:8000 $DOCKER_IMAGE'
                }
            }
        }

        stage('Run Pytest') {
            steps {
                script {
                    // Ejecutar pytest en el contenedor Docker. Asumimos que los tests están en el directorio tests/
                    echo 'Running Pytest...'
                    sh 'docker exec $CONTAINER_NAME pytest tests/'
                }
            }
        }

        stage('Stop Docker Container') {
            steps {
                script {
                    // Detener y remover el contenedor Docker después de ejecutar los tests
                    echo 'Stopping Docker container...'
                    sh 'docker stop $CONTAINER_NAME'
                    sh 'docker rm $CONTAINER_NAME'
                }
            }
        }
    }

    post {
        always {
            // Limpiar los contenedores Docker y las imágenes después de la ejecución
            echo 'Cleaning up Docker containers and images...'
            sh 'docker system prune -f'
        }
        success {
            // Si todo es exitoso, puedes agregar alguna notificación o mensaje
            echo 'Pipeline completed successfully.'
        }
        failure {
            // Si algo falla, muestra el error
            echo 'There was an issue with the pipeline.'
        }
    }
}

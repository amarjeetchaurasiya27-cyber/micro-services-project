pipeline {
    agent any
    environment {
        DOCKER_HUB_USER = "amarjeetchaurasiya"
        BACKEND_IMAGE = "backend-app"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build & Push Backend') {
            steps {
                bat "docker build -t %DOCKER_HUB_USER%/%BACKEND_IMAGE%:latest ./backend"
                withCredentials([usernamePassword(credentialsId: 'docker-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    bat "docker login -u %USER% -p %PASS%"
                    bat "docker push %DOCKER_HUB_USER%/%BACKEND_IMAGE%:latest"
                }
            }
        }
        stage('Deploy to K8s') {
            steps {
                bat "kubectl apply -f db-k8s.yaml"
                bat "kubectl apply -f backend-k8s.yaml"
                bat "kubectl rollout status deployment/backend"
            }
        }
    }
}
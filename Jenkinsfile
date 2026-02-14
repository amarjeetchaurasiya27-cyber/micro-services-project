pipeline {
    agent any

    environment {
        // Aapka DockerHub Username
        DOCKER_USER = "amarjeetchaurasiya" 
        
        // Image names aapke repo ke hisab se
        BACKEND_IMG  = "backend-app"
        FRONTEND_IMG = "frontend-app"
        
        // Build Number ko tag ki tarah use karenge taaki har baar naya version deploy ho
        BUILD_TAG    = "build-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Aapki specific repo se code download hoga
                git branch: 'main', url: 'https://github.com/amarjeetchaurasiya27-cyber/micro-services-project.git'
            }
        }

        stage('Docker Build & Tag') {
            steps {
                echo "Building Images..."
                // Backend aur Frontend images build ho rahi hain
                bat "docker build -t %DOCKER_USER%/%BACKEND_IMG%:%BUILD_TAG% ./backend"
                bat "docker build -t %DOCKER_USER%/%FRONTEND_IMG%:%BUILD_TAG% ./frontend"
                
                // Latest tag bhi de dete hain reference ke liye
                bat "docker tag %DOCKER_USER%/%BACKEND_IMG%:%BUILD_TAG% %DOCKER_USER%/%BACKEND_IMG%:latest"
                bat "docker tag %DOCKER_USER%/%FRONTEND_IMG%:%BUILD_TAG% %DOCKER_USER%/%FRONTEND_IMG%:latest"
            }
        }

        stage('Docker Login & Push') {
            steps {
                // Jenkins Credentials ID 'docker-creds' use kar rahe hain
                withCredentials([usernamePassword(credentialsId: 'docker-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    echo "Logging into Docker Hub..."
                    bat "docker login -u %USER% -p %PASS%"
                    
                    echo "Pushing Images to Docker Hub..."
                    bat "docker push %DOCKER_USER%/%BACKEND_IMG%:%BUILD_TAG%"
                    bat "docker push %DOCKER_USER%/%FRONTEND_IMG%:%BUILD_TAG%"
                    bat "docker push %DOCKER_USER%/%BACKEND_IMG%:latest"
                    bat "docker push %DOCKER_USER%/%FRONTEND_IMG%:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes Cluster..."
                // k8s-manifests folder ke andar ki saari files apply honge
                bat "kubectl apply -f k8s-manifests/"
                
                // Nayi images ko force update karne ke liye rollout restart
                bat "kubectl rollout restart deployment/backend"
                bat "kubectl rollout restart deployment/frontend"
                
                echo "Deployment Status Check..."
                bat "kubectl rollout status deployment/backend"
                bat "kubectl rollout status deployment/frontend"
            }
        }
    }

    post {
        success {
            echo "Congratulations Amarjeet! Pipeline successfully complete ho gayi. 🎉"
        }
        failure {
            echo "Oops! Pipeline fail ho gayi. Console output check karein. ❌"
        }
    }
}

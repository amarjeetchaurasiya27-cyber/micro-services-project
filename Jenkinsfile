pipeline {
    agent any

    environment {
        // Aapka DockerHub Username aur Image Details
        DOCKER_USER  = "amarjeet001" 
        BACKEND_IMG  = "backend-app"
        FRONTEND_IMG = "frontend-app"
        BUILD_TAG    = "build-${BUILD_NUMBER}"
        
        // K8S Configuration - Isse kubectl ko rasta milega
        // DHAYAN DEIN: Agar aapka Windows user 'lenovo' nahi hai, toh ise badal dein
        KUBECONFIG   = "C:/Users/lenovo/.kube/config"
        NO_PROXY     = "localhost,127.0.0.1"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/amarjeetchaurasiya27-cyber/micro-services-project.git'
            }
        }

        stage('Docker Build & Tag') {
            steps {
                echo "Building Images..."
                bat "docker build -t %DOCKER_USER%/%BACKEND_IMG%:%BUILD_TAG% ./backend"
                bat "docker build -t %DOCKER_USER%/%FRONTEND_IMG%:%BUILD_TAG% ./frontend"
                
                bat "docker tag %DOCKER_USER%/%BACKEND_IMG%:%BUILD_TAG% %DOCKER_USER%/%BACKEND_IMG%:latest"
                bat "docker tag %DOCKER_USER%/%FRONTEND_IMG%:%BUILD_TAG% %DOCKER_USER%/%FRONTEND_IMG%:latest"
            }
        }

        stage('Docker Login & Push') {
            steps {
                // Aapka credential ID: dockerhub-creds
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    echo "Logging into Docker Hub..."
                    bat "docker login -u %USER% -p %PASS%"
                    
                    echo "Pushing Images..."
                    bat "docker push %DOCKER_USER%/%BACKEND_IMG%:%BUILD_TAG%"
                    bat "docker push %DOCKER_USER%/%FRONTEND_IMG%:%BUILD_TAG%"
                    bat "docker push %DOCKER_USER%/%BACKEND_IMG%:latest"
                    bat "docker push %DOCKER_USER%/%FRONTEND_IMG%:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                // Proxy bypass ke saath apply karenge
                withEnv(["NO_PROXY=localhost,127.0.0.1", "no_proxy=localhost,127.0.0.1"]) {
                    // Step 1: Cluster connection check
                    bat "kubectl cluster-info"
                    
                    // Step 2: Apply Manifests
                    bat "kubectl apply -f k8s-manifests/ --validate=false"
                    
                    // Step 3: Force update pods
                    echo "Restarting deployments to use new images..."
                    bat "kubectl rollout restart deployment/backend"
                    bat "kubectl rollout restart deployment/frontend"
                }
            }
        }
    }

    post {
        success {
            echo "Mubarak ho Amarjeet! Project Deploy ho gaya. 🎉"
        }
        failure {
            echo "Pipeline fail hui, check logs. ❌"
        }
    }
}

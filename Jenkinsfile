pipeline {
    agent any
    
    environment {
        // Load environment variables from .env file
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'diptech11/python-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_USERNAME = 'diptech11'
        SONARQUBE_URL = 'http://host.docker.internal:9003'
        K8S_NAMESPACE = 'python-app'
        K8S_CLUSTER_CONTEXT = 'kind-python-app-cluster'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out source code..."
                    checkout scm
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    echo "Building Python application..."
                    sh '''
                        python -m venv venv
                        . venv/bin/activate || source venv/Scripts/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo "Running unit tests..."
                    sh '''
                        . venv/bin/activate || source venv/Scripts/activate
                        pytest tests/ --cov=app --cov-report=xml --cov-report=html -v
                    '''
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo "Running SonarQube analysis..."
                    withSonarQubeEnv('SonarQube') {
                        sh '''
                            sonar-scanner \
                              -Dsonar.projectKey=python-app \
                              -Dsonar.projectName="Python Application" \
                              -Dsonar.sources=app \
                              -Dsonar.tests=tests \
                              -Dsonar.python.coverage.reportPaths=coverage.xml \
                              -Dsonar.host.url=${SONARQUBE_URL} \
                              -Dsonar.login=${SONAR_TOKEN}
                        '''
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                script {
                    echo "Waiting for SonarQube quality gate..."
                    timeout(time: 5, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing image to Docker Hub..."
                    sh '''
                        # Load .env file to get DOCKERHUB_TOKEN
                        if [ -f .env ]; then
                            export $(cat .env | xargs)
                        fi
                        
                        # Login to Docker Hub using token from .env
                        echo ${DOCKERHUB_TOKEN} | docker login -u ${DOCKER_USERNAME} --password-stdin
                        
                        # Push images
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        
                        # Logout
                        docker logout
                    '''
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to KIND cluster..."
                    sh '''
                        kubectl config use-context ${K8S_CLUSTER_CONTEXT}
                        
                        # Apply manifests
                        kubectl apply -f k8s/configmap.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        
                        # Update image
                        kubectl set image deployment/python-app \
                          python-app=${DOCKER_IMAGE}:${DOCKER_TAG} \
                          -n ${K8S_NAMESPACE}
                        
                        # Wait for rollout
                        kubectl rollout status deployment/python-app -n ${K8S_NAMESPACE} --timeout=5m
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo "Verifying deployment health..."
                    sh '''
                        kubectl get pods -n ${K8S_NAMESPACE}
                        kubectl get svc -n ${K8S_NAMESPACE}
                        
                        # Wait for pods to be ready
                        kubectl wait --for=condition=ready pod -l app=python-app -n ${K8S_NAMESPACE} --timeout=300s
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "Cleaning up workspace..."
                junit testResults: 'test-results.xml', allowEmptyResults: true
                publishHTML([
                    reportDir: 'htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report',
                    allowMissing: true
                ])
            }
        }
        success {
            script {
                echo "✅ Pipeline completed successfully!"
                echo "Docker image pushed: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo "Deployed to: ${K8S_NAMESPACE} namespace"
                echo "Access at: http://localhost:8000"
            }
        }
        failure {
            script {
                echo "❌ Pipeline failed! Check logs above for details."
                emailext(
                    subject: "Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        Build failed for ${env.JOB_NAME}
                        Build Number: ${env.BUILD_NUMBER}
                        Build URL: ${env.BUILD_URL}
                        
                        Check console output for details.
                    """,
                    to: "${env.CHANGE_AUTHOR_EMAIL}",
                    mimeType: 'text/html'
                )
            }
        }
    }
}

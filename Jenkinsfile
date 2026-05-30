pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/ajiabhinav43-lab/MyWebApp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t mywebapp .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop mywebapp || true'
                sh 'docker rm mywebapp || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                docker run -d \
                --env-file /home/ubuntu/MyWebApp/.env \
                -p 8000:8000 \
                --name mywebapp \
                --restart always \
                mywebapp
                '''
            }
        }
    }
}

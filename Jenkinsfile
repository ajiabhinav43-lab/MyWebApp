pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "abhinav0824/mywebapp:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/ajiabhinav43-lab/MyWebApp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $DOCKER_IMAGE'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@13.202.127.59 << EOF
                    docker pull $DOCKER_IMAGE
                    docker stop mywebapp || true
                    docker rm mywebapp || true
                    docker run -d -p 8000:8000 --name mywebapp $DOCKER_IMAGE
                    EOF
                    '''
                }
            }
        }
    }
}

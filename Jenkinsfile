pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Sreedev895/DevOps-Task-Manager.git'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install -r requirements.txt
                    venv/bin/python -m unittest discover -s tests -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-task-manager:latest .'
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'docker compose up -d --build'
            }
        }
    }
}

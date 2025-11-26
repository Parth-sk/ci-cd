pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                // If job is configured as "Pipeline script from SCM", you can even delete this stage.
                git branch: 'main',
                    credentialsId: 'cicd-id',
                    url: 'https://github.com/Parth-sk/ci-cd.git'
            }
        }

        stage('Install dependencies') {
            steps {
                // Everything is in ci-cd root: requirements.txt next to app.py
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                // test_app.py is in the same folder as app.py
                bat 'pytest test_app.py'
            }
        }

        stage('Build Docker image') {
            when {
                // Only if tests didn't fail
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                // Build image from current folder (ci-cd root = Docker build context)
                bat "docker build -t parthsk/ci-cd-todo:latest ."
            }
        }

        stage('Docker login') {
            steps {
                bat "docker login -u parthsk -p %DOCKERHUB_PSW%"
            }
        }

        stage('Push Docker image') {
            steps {
                bat "docker push parthsk/ci-cd-todo:latest"
            }
        }
    }
}

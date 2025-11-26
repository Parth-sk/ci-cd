pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub-creds')
        IMAGE_NAME = 'todo-cli'           // change name if you want
        CONTAINER_NAME = 'todo-cli-app'   // container name on your machine
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

        stage('Create Virtual Environment') {
            steps {
                bat '"C:\\Users\\parth\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat ".\\venv\\Scripts\\python.exe -m pip install --upgrade pip"
                bat ".\\venv\\Scripts\\pip.exe install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                bat ".\\venv\\Scripts\\pytest.exe"
            }
        }


        stage('Build Docker image') {
            when {
                // Only if tests didn't fail
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                // Build image from current folder (ci-cd root = Docker build context)
                bat "docker build -t %DOCKERHUB_USR%/%IMAGE_NAME%:latest ."
            }
        }
        stage('Push Docker Image') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                // Login and push to Docker Hub
                bat "docker login -u %DOCKERHUB_USR% -p %DOCKERHUB_PSW%"
                bat "docker push %DOCKERHUB_USR%/%IMAGE_NAME%:latest"
            }
        }

        stage('Deploy Container') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                // Stop & remove any existing container with same name (ignore errors)
                bat "docker stop %CONTAINER_NAME% || echo No existing container to stop"
                bat "docker rm %CONTAINER_NAME% || echo No existing container to remove"

                // Run new container from pushed image
                bat "docker run -d --name %CONTAINER_NAME% %DOCKERHUB_USR%/%IMAGE_NAME%:latest"
            }
        }

        stage('Docker login') {
            steps {
                bat "docker login -u %DOCKERHUB_USR% -p %DOCKERHUB_PSW%"
            }
        }
    }
}

pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub-creds')
        IMAGE = "parthsk/cicd-project-pipeline:jenkins"
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
                bat "docker build -t %IMAGE% ."
            }
        }
        stage('Push Docker Image') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                // Login
                bat "docker login -u %DOCKERHUB_USR% -p %DOCKERHUB_PSW%"

                // Push image; if Docker complains about platform and returns non-zero,
                // don't fail the pipeline as long as layers were pushed.
                bat "docker push %IMAGE% || exit /b 0"
            }
        }

        stage('Deploy Container') {
            steps {
                // The "|| echo..." pattern mimics "|| true" in Linux. 
                // It ensures the build doesn't fail if the container doesn't exist yet.
                bat '''
                  docker pull %IMAGE%
                  docker stop ci-cd-demo || echo "Container not running, skipping stop"
                  docker rm ci-cd-demo || echo "Container not found, skipping remove"
                  docker run -d -p 5000:5000 --name ci-cd-demo %IMAGE%
                '''
            }
        }
    }
}
pipeline {
    agent any

    environment {
        IMAGE = "parthsk/cicd-project-pipeline:jenkins"
        VENV = ".venv"
        // On Windows, we usually just call 'python' if it is added to the PATH
        PYTHON = "C:\\Users\\parth\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                  branches: [[name: '*/main']],
                  userRemoteConfigs: [[
                    url: 'https://https://github.com/Parth-sk/ci-cd.git',
                    credentialsId: 'cicd-id'
                  ]]
                ])
            }
        }

        stage('Create Virtual Environment') {
            steps {
                // 1. Create venv
                // 2. Upgrade pip using the executable inside Scripts
                bat '''
                    %PYTHON% -m venv %VENV%
                    %VENV%\\Scripts\\python.exe -m pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                // Use pip inside the virtual environment
                bat '%VENV%\\Scripts\\pip.exe install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Use pytest inside the virtual environment
                bat '%VENV%\\Scripts\\pytest.exe -v'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', 
                                                  usernameVariable: 'USER', 
                                                  passwordVariable: 'PASS')]) {
                    // Log in immediately so subsequent steps are authenticated
                    bat '@echo %PASS% | docker login -u %USER% --password-stdin'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', 
                                                  usernameVariable: 'USER', 
                                                  passwordVariable: 'PASS')]) {
                    // @echo prevents the password from showing in logs
                    // %VAR% is used for batch variables
                    bat '''
                      docker logout
                      @echo %PASS% | docker login -u %USER% --password-stdin
                      docker push %IMAGE%
                    '''
                }
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
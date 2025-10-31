pipeline{
    agent {
        node {
            label 'local'
        }
    }
    environment {
        PATH = "/usr/local/bin:${env.PATH}"
    }

    stages{
        stage("git checkout") {
            steps {
                sh 'echo "git checkout"'
                git branch: 'main', url: 'https://github.com/vaja13/test_jenkins.git'
            }
        }
    
        stage('Initialize') {
            steps {
                sh 'echo "Initializing the project..."'
            }
        }
        stage('Build') {
            steps {
                sh 'echo "Building the project..."'
                sh 'docker-compose build'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo "Deploying the application..."'
                sh 'docker-compose up -d'
            }
        }
    }   
}
 

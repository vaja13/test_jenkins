pipeline{
    agent {
        node {
            label 'local'
        }
    }
    stages{
        stage("git checkout") {
            steps {
                sh 'echo "git checkout"'
                git branch: 'main', url: 'https://github.com/vaja13/test_jenkins.git'
            }
        }
    }
    
    stages {
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
 

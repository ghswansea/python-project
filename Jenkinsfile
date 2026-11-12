pipeline {
    agent any
    stages {
        stage("Build docker image") {
            steps {
                sh 'docker build -t python-project:${BUILD_NUMBER} .'
            }
        }
        stage("Run container test") {
	    steps {
		sh 'docker run --rm python-project:${BUILD_NUMBER}'
    	    }
   	}
    }
    post {
	always {
            sh 'docker rmi python-project:${BUILD_NUMBER} || true'
        }
    }
}

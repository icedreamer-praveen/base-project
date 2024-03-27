pipeline {

	agent any
	environment {
		REGISTRY_URL = credentials('fonenextUrl')
		REGISTRY_USER = credentials('fonenextUser')
		REGISTRY_PASS = credentials('fonenextPass')
		COSIGN_PASSWORD = credentials('cosign-password')
		COSIGN_PRIVATE_KEY = credentials('cosign-private-key')
		SONAR_TOKEN = credentials('sonar_login')

		SONAR_PROJECT_KEY = 'backend'

		DOCKER_FILE_LOCATION = 'Dockerfile'

		DOCKER_IMAGE_REPOSITORY = 'fonenext/backend-dev'
		TAGGED_DOCKER_IMAGE = "$REGISTRY_URL/$DOCKER_IMAGE_REPOSITORY:$BUILD_NUMBER"

		GIT_URL = 'https://gitlab-01.f1soft.com/fonenxt-ai/backend.git'
		GIT_BRANCH = 'dev'
		GIT_CREDEITIALS_ID = 'fonenext-git'

		DEPLOY_USER = credentials('deployerUser')
		DEPLOYER = credentials('deployerPass')
	}
	options {
		buildDiscarder(logRotator(artifactNumToKeepStr: '5', numToKeepStr: '5'))
	 }

	stages {
		stage('Git Clone') {
			when {
                expression { BRANCH_NAME ==~ /($GIT_BRANCH)/ }
			}
			steps {
				git branch: "$GIT_BRANCH", changelog: false, credentialsId: "$GIT_CREDEITIALS_ID", poll: false, url: "$GIT_URL"
				
			}
		}
		stage('Docker Build') {
			when {
                expression { BRANCH_NAME ==~ /($GIT_BRANCH)/ }
			}
			parallel {
				stage('Build') {
					steps {
						dockerBuildPush('$DOCKER_IMAGE_REPOSITORY', '$DOCKER_FILE_LOCATION')
					}
				}
			}	
		}
		stage('Cosign') {
			when {
                expression { BRANCH_NAME ==~ /($GIT_BRANCH)/ }
			}
			steps {
				sh 'echo -n $COSIGN_PASSWORD | cosign sign --key $COSIGN_PRIVATE_KEY $TAGGED_DOCKER_IMAGE'
			}
        }
		stage('Delete Docker Image') {
			when {
                expression { BRANCH_NAME ==~ /($GIT_BRANCH)/ }
			}
            steps {
                sh 'docker rmi $TAGGED_DOCKER_IMAGE'
            }
        }
	}

	post {
		success {
            script {
                if (BRANCH_NAME ==~ /($GIT_BRANCH)/) {
                    sh """
                        rm -rf /var/jenkins_home/workspace/backend_dev/fonenext-argocd

						mkdir -p /var/jenkins_home/workspace/backend_dev/fonenext-argocd && cd /var/jenkins_home/workspace/backend_dev/fonenext-argocd
						git clone https://$DEPLOY_USER:$DEPLOYER@gitlab-01.f1soft.com/uat-kubernetes/uat-argocd/fonenext.git

						sed -i -e  "s,dev-registry.f1soft.com/fonenext/backend-dev:.*,dev-registry.f1soft.com/fonenext/backend-dev:$BUILD_NUMBER,g" /var/jenkins_home/workspace/backend_dev/fonenext-argocd/fonenext/fonenext-dev/Deployments/dep-backend.yml

						cd /var/jenkins_home/workspace/backend_dev/fonenext-argocd/fonenext

						git add .
						git commit -m "Update app image tag of backend-dev to $BUILD_NUMBER"
						git push origin main --repo https://$DEPLOY_USER:$DEPLOYER@gitlab-01.f1soft.com/uat-kubernetes/uat-argocd/fonenext.git

						rm -rf /var/jenkins_home/workspace/backend_dev/fonenext-argocd
                    """
                }
            }
        }
		always {
			cleanWs()
		}
	}
}

def dockerBuildPush(name, dockerfile, push=true)
{
	sh 'docker build . --network host --file "'+dockerfile+'" -t $REGISTRY_URL/'+name+':$BUILD_NUMBER'
    if (push) {
        sh 'docker login -u $REGISTRY_USER -p $REGISTRY_PASS $REGISTRY_URL'
        sh 'docker push $REGISTRY_URL/'+name+':$BUILD_NUMBER'
    }
}

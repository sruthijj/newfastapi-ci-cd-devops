pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        DOCKER_CREDENTIALS_ID = 'docker-cred'
        DOCKER_IMAGE          = 'sruthijj/fastapi-app'
        SONAR_SERVER_NAME     = 'Sonarqube_env'
        SONAR_SCANNER_TOOL    = 'sonar-scanner'
        GIT_CREDENTIALS_ID    = 'github-cred'
        MANIFEST_REPO         = 'https://github.com/sruthijj/maker.git'
        MANIFEST_BRANCH       = 'main'
        MANIFEST_FILE         = 'manifests/deployment.yaml'
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool "${SONAR_SCANNER_TOOL}"
                    def sourcesDir  = fileExists('my_fastapi_app') ? 'my_fastapi_app' : '.'
                    withSonarQubeEnv("${SONAR_SERVER_NAME}") {
                        sh "${scannerHome}/bin/sonar-scanner \
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.projectKey=fastapi-key \
                            -Dsonar.projectName='fastapi-project' \
                            -Dsonar.sources=${sourcesDir}"
                    }
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    def buildContext = fileExists('my_fastapi_app/Dockerfile') ? 'my_fastapi_app' : '.'
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        def appImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}", "${buildContext}")
                        appImage.push()
                        appImage.push('latest')
                    }
                }
            }
        }

        stage('Update Manifest Repo') {
            steps {
                dir('manifest-workspace') {
                    git branch: "${MANIFEST_BRANCH}",
                        credentialsId: "${GIT_CREDENTIALS_ID}",
                        url: "${MANIFEST_REPO}"

                    // The github-cred password must be a GitHub Personal Access Token with repo write scope.
                    withCredentials([usernamePassword(
                            credentialsId: "${GIT_CREDENTIALS_ID}",
                            usernameVariable: 'GIT_USER',
                            passwordVariable: 'GIT_PASS')]) {
                        // Single quotes: secrets are expanded by the shell, not interpolated by Groovy
                        sh '''
                            set -e

                            if [ ! -f "$MANIFEST_FILE" ]; then
                                echo "ERROR: $MANIFEST_FILE not found in manifest repo"
                                exit 1
                            fi

                            # Replace the image line for this app, keeping its indentation
                            sed -i "s|image:.*${DOCKER_IMAGE}.*|image: ${DOCKER_IMAGE}:${BUILD_NUMBER}|" "$MANIFEST_FILE"

                            if git diff --quiet; then
                                echo "No manifest changes to commit."
                            else
                                git -c user.name="Jenkins CI" -c user.email="jenkins@ci.local" \
                                    commit -am "chore(manifest): update fastapi-app image tag to ${BUILD_NUMBER} [skip ci]"
                                git push "https://${GIT_USER}:${GIT_PASS}@${MANIFEST_REPO#https://}" "HEAD:${MANIFEST_BRANCH}"
                            fi
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully! Manifest repo updated with new image tag.'
        }
        failure {
            echo 'Pipeline failed. Please review the stage logs above.'
        }
    }
}

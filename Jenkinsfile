pipeline {
    agent any

    triggers {
        // Jenkins đang chạy local nên dùng polling; không cần expose webhook ra Internet.
        pollSCM('H/5 * * * *')
    }

    options {
        disableConcurrentBuilds()
        timeout(time: 45, unit: 'MINUTES')
        timestamps()
    }

    tools {
        nodejs 'NodeJS'
    }
    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        BACKEND_DIR    = 'backend/web-api'
        FRONTEND_DIR   = 'frontend'
    }
    stages {

        stage('Cleanup Stale Reports') {
            steps {
                sh 'find . -path "*/.scannerwork/report-task.txt" -delete || true'
                sh 'find . -path "*/build/sonar/report-task.txt" -delete || true'
            }
        }

        // BACKEND

        stage('Backend - Build & Test') {
            steps {
                dir("${BACKEND_DIR}") {
                    sh './gradlew clean build'
                }
            }
            post {
                always {
                    junit "${BACKEND_DIR}/build/test-results/test/*.xml"
                    jacoco execPattern: "${BACKEND_DIR}/build/jacoco/test.exec",
                           classPattern: "${BACKEND_DIR}/build/classes/java/main",
                           sourcePattern: "${BACKEND_DIR}/src/main/java"
                }
            }
        }

        stage('Backend - SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    withSonarQubeEnv('SonarQube') {
                        dir("${BACKEND_DIR}") {
                            sh './gradlew sonar -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.token=$SONAR_TOKEN'
                        }
                    }
                }
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // FRONTEND

        stage('Frontend - Install') {
            steps {
                dir("${FRONTEND_DIR}") {
                    sh 'npm ci'
                }
            }
        }

        stage('Frontend - Lint') {
            steps {
                dir("${FRONTEND_DIR}") {
                    sh 'npm run lint'
                }
            }
        }

        stage('Frontend - Test') {
            steps {
                dir("${FRONTEND_DIR}") {
                    sh 'npm run test -- --ci --coverage'
                }
            }
            post {
                always {
                    publishHTML(target: [
                        reportDir:   "${FRONTEND_DIR}/coverage/lcov-report",
                        reportFiles: 'index.html',
                        reportName:  'Frontend Coverage',
                        allowMissing: true
                    ])
                }
            }
        }

        stage('Frontend - Build') {
            steps {
                dir("${FRONTEND_DIR}") {
                    sh 'npm run build'
                }
            }
        }

        stage('Frontend - SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                        dir("${FRONTEND_DIR}") {
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=recruitify-frontend \
                                -Dsonar.sources=src \
                                -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
                            """
                        }
                    }
                }
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            cleanWs()
        }
    }
}

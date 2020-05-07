def getImageTag(String branch) {
  if (branch ==~ "^[A-Za-z]{1,3}-\\d+.*") { 
    // This regex truncates the branch name if its a JIRA Ticket ID (eg. SPT-3777)
    def escaped_branch = (branch.replace("/", "_") =~ "^[A-Za-z]{1,3}-\\d+")
    return escaped_branch[0]
  } else {
    return branch.replace("/", "_")
  }
}

pipeline {

  agent {
    kubernetes {
      cloud 'eks-swimlane-io'
      label "jenkins-k8s-${UUID.randomUUID().toString()}"
      yaml """
kind: Pod
metadata:
  name: jenkins-k8s
spec:
  securityContext:
    runAsUser: 1001
  containers:
  - name: jnlp
    image: 'jenkins/jnlp-slave:latest'
  - name: jenkins-linux-slave
    image: 'nexus.swimlane.io:5000/jenkins-linux-slave:PR-19-1'
    command: ["tail", "-f", "/dev/null"]
    resources:
      requests:
        memory: "4000Mi"
        cpu: "2000m"
      limits:
        memory: "4000Mi"
        cpu: "2000m"
  imagePullSecrets:
  - name: swimlane-nexus
"""
    }
  }

  parameters {
    booleanParam(name: 'PUBLISH_BRANCH_TO_NEXUS', defaultValue: false, description: 'Do you want to publish the python wheel for this branch to Nexus?')
  }

  environment {
    GIT_COMMIT_SHORT = "${env.GIT_COMMIT[0..7]}"
    ACTUAL_BRANCH = "${env.CHANGE_BRANCH ?: env.BRANCH_NAME}"
    IMAGE_BRANCH = getImageTag(env.ACTUAL_BRANCH)
    CODACY_PROJECT_TOKEN = credentials('codacy-project-token-swimlane-python')
  }

  options {
    disableConcurrentBuilds()
    timeout(time: 15, unit: 'MINUTES')
    timestamps()
    buildDiscarder(logRotator(artifactNumToKeepStr: '1'))
  }

  stages {
    stage('Build') {
      failFast true

      parallel {
        stage('Python 2.7') {
          agent {
            kubernetes {
              cloud 'eks-swimlane-io'
              label "jenkins-k8s-${UUID.randomUUID().toString()}"
              yaml """
kind: Pod
metadata:
  name: jenkins-k8s
spec:
  securityContext:
    runAsUser: 1001
  containers:
  - name: jnlp
    image: 'jenkins/jnlp-slave:latest'
  - name: jenkins-linux-slave
    image: 'nexus.swimlane.io:5000/jenkins-linux-slave:PR-19-1'
    command: ["tail", "-f", "/dev/null"]
    resources:
      requests:
        memory: "4000Mi"
        cpu: "2000m"
      limits:
        memory: "4000Mi"
        cpu: "2000m"
  imagePullSecrets:
  - name: swimlane-nexus
"""
            }
          }

          stages {
            stage('Install dependencies') {
              steps {
                container('jenkins-linux-slave'){
                  sh('/usr/local/bin/pip2.7 install -U -r requirements.txt')
                  sh('/usr/local/bin/pip2.7 install -U -r test-requirements.txt')
                  sh('/usr/local/bin/pip2.7 install codacy-coverage')
                }
              }
            }
            stage('Test') {
              steps {
                container('jenkins-linux-slave'){
                  sh('/home/build-user/.local/bin/py.test -v --cov=swimlane --cov-report=xml')
                  sh('/home/build-user/.local/bin/python-codacy-coverage -r coverage.xml')
                }
              }
            }
            stage('Build') {
              steps {
                container('jenkins-linux-slave'){
                  sh('python2.7 offline_installer/build_installer.py')
                }
              }
            }
          }
        }
        stage ('Python 3.6') {
          agent {
            kubernetes {
              cloud 'eks-swimlane-io'
              label "jenkins-k8s-${UUID.randomUUID().toString()}"
              yaml """
kind: Pod
metadata:
  name: jenkins-k8s
spec:
  securityContext:
    runAsUser: 1001
  containers:
  - name: jnlp
    image: 'jenkins/jnlp-slave:latest'
  - name: jenkins-linux-slave
    image: 'nexus.swimlane.io:5000/jenkins-linux-slave:PR-19-1'
    command: ["tail", "-f", "/dev/null"]
    resources:
      requests:
        memory: "4000Mi"
        cpu: "2000m"
      limits:
        memory: "4000Mi"
        cpu: "2000m"
  imagePullSecrets:
  - name: swimlane-nexus
"""
            }
          }

          stages {
            stage('Install dependencies') {
              steps {
                container('jenkins-linux-slave'){
                  sh('/usr/local/bin/pip3.6 install --user -U -r requirements.txt')
                  sh('/usr/local/bin/pip3.6 install --user -U -r test-requirements.txt')
                  sh('/usr/local/bin/pip3.6 install --user codacy-coverage')
                }
              }
            }
            stage('Test') {
              steps {
                container('jenkins-linux-slave'){
                  sh('/home/build-user/.local/bin/py.test -v --cov=swimlane --cov-report=xml')
                  sh('/home/build-user/.local/bin/python-codacy-coverage -r coverage.xml')
                }
              }
            }
            stage('Build') {
              steps {
                container('jenkins-linux-slave'){
                  sh('/usr/local/bin/python3.6 offline_installer/build_installer.py')
                }
              }
            }
          }
        }
      }
    }
    stage ('Publish to Nexus') {
      when{
        anyOf{
          branch 'master'
          branch 'hotfix-*'
          branch 'release-*'
          expression { return params.PUBLISH_BRANCH_TO_NEXUS }
        }
      }

      steps {
        container('jenkins-linux-slave'){
          sh('echo hi')
        }
      }
    }
    stage('Publish') {
      when {
        buildingTag()
      }

      stages {
        stage('Create Github Release') {
          steps {
            container('jenkins-linux-slave'){
              sh('echo hi')
            }
          }
        }
        stage('Push to pypi') {
          steps {
            container('jenkins-linux-slave'){
              sh('echo hi')
            }
          }
        }
      }
    }
  }

  post {
    always {
      cleanWs()
    }
    regression {
      script {
        if ("${env.BRANCH_NAME}" == "master" || "${env.BRANCH_NAME}" ==~ "^release-.*" || "${env.BRANCH_NAME}" ==~ "^hotfix-.*") {
          slackSend(
            baseUrl: 'https://swimlane.slack.com/services/hooks/jenkins-ci/',
            channel: '#platform_notification',
            color: 'danger',
            message: "@here Swimlane-python pipeline on branch ${env.ACTUAL_BRANCH} has failed and is now RED: <${env.RUN_DISPLAY_URL}|Build #${env.BUILD_NUMBER} git commit ${GIT_COMMIT_SHORT}> ",
            teamDomain: 'swimlane',
            tokenCredentialId: 'slack-token')
        }
      }
    }
    fixed {
      script {
        if ("${env.BRANCH_NAME}" == "master" || "${env.BRANCH_NAME}" ==~ "^release-.*" || "${env.BRANCH_NAME}" ==~ "^hotfix-.*") {
          slackSend(
            baseUrl: 'https://swimlane.slack.com/services/hooks/jenkins-ci/',
            channel: '#platform_notification',
            color: 'good',
            message: "@here Swimlane-python pipeline on branch ${env.ACTUAL_BRANCH} has passed and is now GREEN: <${env.RUN_DISPLAY_URL}|Build #${env.BUILD_NUMBER} git commit ${GIT_COMMIT_SHORT}> ",
            teamDomain: 'swimlane',
            tokenCredentialId: 'slack-token')
        }
      }
    }
  }
}
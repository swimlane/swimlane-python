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
    image: 'nexus.swimlane.io:5000/jenkins-linux-slave:PR-19-6'
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
    booleanParam(name: 'PUBLISH_BRANCH_TO_S3', defaultValue: false, description: 'Do you want to publish the 2.7 offline for this branch to S3?')
  }

  environment {
    PLATFORM_SEMVER = "10.1.2"
    SWIMLANE_PYTHON_SEMVER = "10.1.3"
    GIT_COMMIT_SHORT = "${env.GIT_COMMIT[0..7]}"
    ACTUAL_BRANCH = "${env.CHANGE_BRANCH ?: env.BRANCH_NAME}"
    IMAGE_BRANCH = getImageTag(env.ACTUAL_BRANCH)
    CODACY_PROJECT_TOKEN = credentials('codacy-project-token-swimlane-python')
    GIT_CREDENTIALS = credentials('github-jenkins-pat-new')
    GITHUB_USER = "${env.GIT_CREDENTIALS_USR}"
    GITHUB_PASSWORD = "${env.GIT_CREDENTIALS_PSW}"
  }

  options {
    disableConcurrentBuilds()
    timeout(time: 15, unit: 'MINUTES')
    timestamps()
    buildDiscarder(logRotator(artifactNumToKeepStr: '1'))
  }

  stages {
    stage('Build offline installers') {
      failFast true

      parallel {
        stage('Python 2.7') {
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
                  // Rename the dist directory so it doesn't conflict with the dist dir that is created during the wheel build
                  sh('mv dist offline-installers')
                  archiveArtifacts(artifacts: "offline-installers/*")
                  stash includes: 'offline-installers/*', name: 'py27-installer'
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
    image: 'nexus.swimlane.io:5000/jenkins-linux-slave:PR-19-6'
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
                  // Rename the dist directory so it doesn't conflict with the dist dir that is created during the wheel build
                  sh('mv dist offline-installers')
                  archiveArtifacts(artifacts: "offline-installers/*")
                  stash includes: 'offline-installers/*', name: 'py36-installer'
                }
              }
            }
          }
        }
      }
    }
    stage ('Build wheel') {
      steps {
        container('jenkins-linux-slave'){
          sh("rm -rf dist")
          sh 'python /usr/local/bin/jj2.py -v NEXUS_USER=${NEXUS_USER} -v NEXUS_PASSWORD=${NEXUS_PASSWORD} -v PYPI_USER=${PYPI_USER} -v PYPI_PASSWORD=${PYPI_PASSWORD} pypirc.jinja2 > .pypirc'

          sh('python2.7 setup.py sdist bdist_wheel')

          archiveArtifacts(artifacts: "dist/*")
        }
      }
    }
    stage ('Publish to Nexus') {
      when{
        anyOf{
          buildingTag()
          branch 'master'
          branch 'hotfix-*'
          branch 'release-*'
          expression { return params.PUBLISH_BRANCH_TO_NEXUS }
        }
      }

      steps {
        container('jenkins-linux-slave'){
          withCredentials([usernamePassword(credentialsId: 'nexusLogin', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASSWORD'),
          usernamePassword(credentialsId: 'pypiLogin', usernameVariable: 'PYPI_USER', passwordVariable: 'PYPI_PASSWORD')]) {
            sh('twine upload --repository-url https://nexus.swimlane.io/repository/pypi/ -u ${NEXUS_USER} -p ${NEXUS_PASSWORD} dist/*')
            slackSend(
              baseUrl: 'https://swimlane.slack.com/services/hooks/jenkins-ci/',
              channel: '#platform_notification',
              color: 'good',
              message: """\
Swimlane-python has been pushed to Nexus for branch ${ACTUAL_BRANCH} commit ${GIT_COMMIT_SHORT}
              """.stripIndent(),
              teamDomain: 'swimlane',
              tokenCredentialId: 'slack-token')
          }
        }
      }
    }
    stage ('Publish branch to S3') {
      when{
        anyOf{
          branch 'master'
          branch 'hotfix-*'
          branch 'release-*'
          expression { return params.PUBLISH_BRANCH_TO_S3 }
        }
      }

      steps {
        container('jenkins-linux-slave'){
          withAWS(region:'us-west-2', credentials: 'aws-publish-key') {
            s3Upload(file:"offline-installers/swimlane-python-${SWIMLANE_PYTHON_SEMVER}-offline-installer-win_amd64-py27.pyz", bucket:'swimlane-builds', path:"python_driver/${ACTUAL_BRANCH}/${PLATFORM_SEMVER}/")
            script {
              env.OFFLINE_INSTALLER_LINK = sh (script: "aws s3 presign s3://swimlane-builds/python_driver/${ACTUAL_BRANCH}/${PLATFORM_SEMVER}/swimlane-python-${SWIMLANE_PYTHON_SEMVER}-offline-installer-win_amd64-py27.pyz --expires-in 157680000", returnStdout: true).trim()
              slackSend(
                baseUrl: 'https://swimlane.slack.com/services/hooks/jenkins-ci/',
                channel: '#platform_notification',
                color: 'good',
                message: """\
  Swimlane-python offline installer has been uploaded to S3 for branch ${ACTUAL_BRANCH} commit ${GIT_COMMIT_SHORT}
  ${env.OFFLINE_INSTALLER_LINK}
                """.stripIndent(),
                teamDomain: 'swimlane',
                tokenCredentialId: 'slack-token')
            }
          }
        }
      }
    }
    stage('Publish') {
      when {
        buildingTag()
      }

      stages {
        stage ('Publish to S3') {
          steps {
            container('jenkins-linux-slave'){
              withAWS(region:'us-west-2', credentials: 'aws-publish-key') {
                s3Upload(file:"offline-installers/swimlane-python-${SWIMLANE_PYTHON_SEMVER}-offline-installer-win_amd64-py27.pyz", bucket:'swimlane-builds', path:"python_driver/${ACTUAL_BRANCH}/${PLATFORM_SEMVER}/")
                script {
                  env.OFFLINE_INSTALLER_LINK = sh (script: "aws s3 presign s3://swimlane-builds/python_driver/${PLATFORM_SEMVER}/swimlane-python-${SWIMLANE_PYTHON_SEMVER}-offline-installer-win_amd64-py27.pyz --expires-in 157680000", returnStdout: true).trim()
                  slackSend(
                    baseUrl: 'https://swimlane.slack.com/services/hooks/jenkins-ci/',
                    channel: '#platform_notification',
                    color: 'good',
                    message: """\
Swimlane-python offline installer has been uploaded to S3 for version ${TAG_NAME} commit ${GIT_COMMIT_SHORT}
${env.OFFLINE_INSTALLER_LINK}
                    """.stripIndent(),
                    teamDomain: 'swimlane',
                    tokenCredentialId: 'slack-token')
                }
              }
            }
          }
        }
        stage('Push to pypi') {
          steps {
            container('jenkins-linux-slave'){
              withCredentials([usernamePassword(credentialsId: 'nexusLogin', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASSWORD'),
              usernamePassword(credentialsId: 'pypiLogin', usernameVariable: 'PYPI_USER', passwordVariable: 'PYPI_PASSWORD')]) {
                sh('twine upload -u ${PYPI_USER} -p ${PYPI_PASSWORD} dist/*')
                slackSend(
                  baseUrl: 'https://swimlane.slack.com/services/hooks/jenkins-ci/',
                  channel: '#platform_notification',
                  color: 'good',
                  message: """\
Swimlane-python has been pushed to Pypi for ${TAG_NAME} commit ${GIT_COMMIT_SHORT}
              """.stripIndent(),
                  teamDomain: 'swimlane',
                  tokenCredentialId: 'slack-token')
              }
            }
          }
        }
        stage('Create Github Release') {
          steps {
            container('jenkins-linux-slave'){
              unstash 'py27-installer'
              unstash 'py36-installer'

              // The same filename can't be attached to a release multiple times so if a tagged build needs to be run again 
              // the old attachments will need to be deleted from the release first
              sh("hub release edit -a offline-installers/swimlane-python-${SWIMLANE_PYTHON_SEMVER}-offline-installer-win_amd64-py27.pyz -a offline-installers/swimlane-python-${SWIMLANE_PYTHON_SEMVER}-offline-installer-win_amd64-py36.pyz -m '' ${TAG_NAME}")
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
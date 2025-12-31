pipeline {
    agent { label 'MeteoAgent' }

    // Los triggers van arriba, fuera de los stages
    triggers {
        cron('0 13 * * 1,2,4,5')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verificar Archivos') {
            steps {
                echo "Trabajando en: ${WORKSPACE}"
                bat 'dir'
            }
        }

        stage('Entorno e Instala dependencias') {
            steps {
                bat '''
                @echo off
                if not exist venv ( python -m venv venv )
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Descargar Datos Meteo') {
            steps {
                bat '''
                @echo off
                call venv\\Scripts\\activate
                python -m src.jobs.meteo_download
                '''
            }
        }
    }
}

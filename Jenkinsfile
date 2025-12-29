pipeline {
    agent { label 'MeteoAgent' }

    stages {

        stage('Checkout') {
            steps {
                // Descarga el código del repositorio automáticamente
                checkout scm
            }
        }

        stage('Verificar Archivos') {
            steps {
                echo "Trabajando en: ${WORKSPACE}"
                bat 'dir' // Esto confirmará que ves tus archivos .py y el requirements.txt
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


    // Configuración del cron: Minuto Hora Día Mes Día_de_la_semana
    triggers {
        cron('0 13 * * *')
    }

    stages {
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
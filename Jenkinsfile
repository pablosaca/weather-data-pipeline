pipeline {
    agent { label 'MeteoAgent' }

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
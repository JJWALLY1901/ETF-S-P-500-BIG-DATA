#!/bin/bash
# Ruta base del proyecto
PROJECT_DIR="/home/ubuntu/etf_proyecto"

# Activar entorno virtual
source $PROJECT_DIR/etfenv/bin/activate

# Ejecutar scripts cada día a las 8 AM
0 8 * * * python $PROJECT_DIR/scripts/data_collection/descargar_alpha.py >> $PROJECT_DIR/logs/alpha.log 2>&1
0 8 * * * python $PROJECT_DIR/scripts/data_collection/twitter_scraper.py >> $PROJECT_DIR/logs/twitter.log 2>&1
0 8 * * * python $PROJECT_DIR/scripts/data_collection/reddit_scraper.py >> $PROJECT_DIR/logs/reddit.log 2>&1

# Procesamiento con Spark cada día a las 9 AM
0 9 * * * spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.0.5 $PROJECT_DIR/scripts/spark_processing/spark_mongo_alpha.py >> $PROJECT_DIR/logs/spark_alpha.log 2>&1
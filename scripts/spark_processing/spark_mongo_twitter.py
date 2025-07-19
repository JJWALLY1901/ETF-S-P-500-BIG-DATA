from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, to_timestamp
import os
from dotenv import load_dotenv

load_dotenv()

def process_twitter_data():
    spark = SparkSession.builder \
        .appName("ProcessTwitterData") \
        .config("spark.mongodb.input.uri", os.getenv('MONGO_URI') + "/bigdata_db.twitter") \
        .config("spark.mongodb.output.uri", os.getenv('MONGO_URI') + "/bigdata_db.twitter_processed") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.0.5") \
        .getOrCreate()

    try:
        # Definir esquema para los tweets
        schema = StructType([
            StructField("id", StringType(), True),
            StructField("text", StringType(), True),
            StructField("created_at", TimestampType(), True),
            StructField("author_id", StringType(), True),
            StructField("retweets", IntegerType(), True),
            StructField("likes", IntegerType(), True),
            StructField("hashtags", ArrayType(StringType()), True),
            StructField("lang", StringType(), True),
            StructField("processed_at", TimestampType(), True)
        ])
        
        # Leer datos de MongoDB
        df = spark.read.format("mongo").load()
        
        # Procesar los datos
        processed_df = df.withColumn("created_ts", 
                              to_timestamp(col("created_at"))) \
                     .withColumn("processed_at", 
                              to_timestamp(col("created_at"))) \
                     .drop("created_at")
        
        # Filtrar tweets en español con más de 10 retweets
        filtered_df = processed_df.filter((col("lang") == "es") & (col("retweets") > 10))
        
        # Extraer hashtags del texto
        from pyspark.sql.functions import regexp_extract_all
        
        hashtag_df = filtered_df.withColumn(
            "hashtags", 
            regexp_extract_all(col("text"), r"#(\w+)", 1)
        )
        
        # Mostrar muestra de datos
        print("=== Muestra de tweets procesados ===")
        hashtag_df.orderBy(col("created_ts").desc()).show(10, truncate=False)
        
        # Guardar en MongoDB
        hashtag_df.write.format("mongo") \
            .mode("overwrite") \
            .save()
            
        print("Tweets procesados y guardados exitosamente")
        
    except Exception as e:
        print(f"Error al procesar tweets: {str(e)}")
    finally:
        spark.stop()

if __name__ == "__main__":
    process_twitter_data()
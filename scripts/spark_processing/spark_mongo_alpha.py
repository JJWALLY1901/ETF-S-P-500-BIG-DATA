from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, to_date
import os
from dotenv import load_dotenv

load_dotenv()

def process_alpha_data():
    spark = SparkSession.builder \
        .appName("ProcessAlphaData") \
        .config("spark.mongodb.input.uri", os.getenv('MONGO_URI') + "/bigdata_db.alpha") \
        .config("spark.mongodb.output.uri", os.getenv('MONGO_URI') + "/bigdata_db.alpha_processed") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.0.5") \
        .getOrCreate()

    try:
        # Esquema para los datos procesados
        schema = StructType([
            StructField("symbol", StringType(), True),
            StructField("date", DateType(), True),
            StructField("open", DoubleType(), True),
            StructField("high", DoubleType(), True),
            StructField("low", DoubleType(), True),
            StructField("close", DoubleType(), True),
            StructField("volume", LongType(), True)
        ])
        
        # Leer datos de MongoDB
        df = spark.read.format("mongo").load()
        
        # Procesar los datos
        processed_data = df.rdd.flatMap(lambda row: [
            {
                "symbol": row["Meta Data"]["2. Symbol"],
                "date": date,
                "open": float(daily_data["1. open"]),
                "high": float(daily_data["2. high"]),
                "low": float(daily_data["3. low"]),
                "close": float(daily_data["4. close"]),
                "volume": int(daily_data["5. volume"])
            }
            for date, daily_data in row["Time Series (Daily)"].items()
        ])
        
        # Crear DataFrame final
        result_df = spark.createDataFrame(processed_data, schema)
        
        # Mostrar muestra de datos
        result_df.orderBy(col("date").desc()).show(10)
        
        # Guardar en MongoDB
        result_df.write.format("mongo") \
            .mode("overwrite") \
            .save()
            
    finally:
        spark.stop()

if __name__ == "__main__":
    process_alpha_data()
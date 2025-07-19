# **Proyecto Big Data - Análisis del ETF S&P 500**  
**Sistema de ingesta, procesamiento y visualización de datos financieros y de redes sociales**  

---

## **📌 Tabla de Contenidos**  
1. [**Descripción del Proyecto**](#-descripción-del-proyecto)  
3. [**Guía de Instalación y Configuración**](#-guía-de-instalación-y-configuración)  
   - [Requisitos Previos](#requisitos-previos)  
   - [Configuración de AWS EC2](#configuración-de-aws-ec2)  
   - [Instalación de Python y Entorno Virtual](#instalación-de-python-y-entorno-virtual)  
   - [Configuración de MongoDB](#configuración-de-mongodb)  
   - [Instalación de Apache NiFi](#instalación-de-apache-nifi)  
   - [Instalación de Apache Spark](#instalación-de-apache-spark)  
4. [**Ejecución de Scripts**](#-ejecución-de-scripts)  
   - [Recolección de Datos (Alpha Vantage, Twitter, Reddit)](#recolección-de-datos-alpha-vantage-twitter-reddit)  
   - [Procesamiento con Spark](#procesamiento-con-spark)  
5. [**Visualización con Metabase**](#-visualización-con-metabase)  
6. [**Automatización con Cron](#-automatización-con-cron)  
7. [**Estructura del Repositorio**](#-estructura-del-repositorio)  
8. [**Licencia**](#-licencia)  

---

## **📌 Descripción del Proyecto**  
Este proyecto permite recolectar, procesar y visualizar datos financieros del **ETF S&P 500** (SPY) y datos de redes sociales (Twitter, Reddit) para analizar correlaciones entre el mercado bursátil y el sentimiento social.  

**Componentes principales:**  
✅ **Ingesta de datos:**  
- Alpha Vantage (datos financieros históricos).  
- Twitter API (tweets con hashtags relacionados).  
- Reddit API (publicaciones en subreddits financieros).  

✅ **Procesamiento con Apache Spark:**  
- Limpieza y transformación de datos.  
- Almacenamiento en MongoDB.  

✅ **Automatización con Apache NiFi:**  
- Flujo automatizado de ingesta de datos.  

✅ **Visualización con Metabase:**  
- Dashboards interactivos con gráficos financieros y análisis de redes sociales.    

---

## **📌 Guía de Instalación y Configuración**  

### **Requisitos Previos**  
- **Cuenta AWS** (para EC2 y servicios relacionados).  
- **Python 3.8+** (para ejecutar los scripts).  
- **MongoDB** (base de datos NoSQL).  
- **Apache NiFi** (automatización de flujos de datos).  
- **Apache Spark** (procesamiento distribuido).  

---

### **🔹 Configuración de AWS EC2**  
1. **Crear una instancia EC2 (Ubuntu 22.04 LTS)**  
   - Tipo de instancia: `t2.micro` (Free Tier).  
   - Grupo de seguridad: Habilitar puertos **22 (SSH), 8080 (NiFi), 27017 (MongoDB), 3000 (Metabase)**.  
   - Clave SSH: Generar o usar una existente.  

2. **Conectarse por SSH**  
   ```bash
   ssh -i "tu-key.pem" ubuntu@<IP_PUBLICA_EC2>
   ```  

---

### **🔹 Instalación de Python y Entorno Virtual**  
1. **Actualizar el sistema e instalar Python**  
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip python3-venv -y
   ```  

2. **Crear entorno virtual**  
   ```bash
   python3 -m venv etfenv
   source etfenv/bin/activate
   ```  

3. **Instalar dependencias**  
   ```bash
   pip install requests python-dotenv tweepy praw pyspark
   ```  

---

### **🔹 Configuración de MongoDB**  
1. **Instalar MongoDB**  
   ```bash
   sudo apt install mongodb -y
   sudo systemctl start mongodb
   sudo systemctl enable mongodb
   ```  

2. **Crear base de datos y colecciones**  
   ```bash
   mongo
   > use bigdata_db
   > db.createCollection("alpha")
   > db.createCollection("twitter")
   > db.createCollection("reddit")
   ```  

---

### **🔹 Instalación de Apache NiFi**  
1. **Descargar e instalar NiFi**  
   ```bash
   wget https://downloads.apache.org/nifi/1.25.0/nifi-1.25.0-bin.tar.gz
   tar -xvf nifi-1.25.0-bin.tar.gz
   cd nifi-1.25.0/bin
   ./nifi.sh start
   ```  

2. **Acceder a la interfaz**  
   Abrir en el navegador:  
   ```
   http://<IP_PUBLICA_EC2>:8080/nifi
   ```  

---

### **🔹 Instalación de Apache Spark**  
1. **Descargar Spark**  
   ```bash
   wget https://downloads.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
   tar -xvf spark-3.4.1-bin-hadoop3.tgz
   ```  

2. **Configurar variables de entorno**  
   ```bash
   echo 'export SPARK_HOME=~/spark-3.4.1-bin-hadoop3' >> ~/.bashrc
   echo 'export PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc
   source ~/.bashrc
   ```  

---

## **📌 Ejecución de Scripts**  

### **🔹 Recolección de Datos (Alpha Vantage, Twitter, Reddit)**  
1. **Alpha Vantage** (`descargar_alpha.py`)  
   ```bash
   python3 descargar_alpha.py
   ```  

2. **Twitter** (`twitter_scraper.py`)  
   ```bash
   python3 twitter_scraper.py
   ```  

3. **Reddit** (`reddit_scraper.py`)  
   ```bash
   python3 reddit_scraper.py
   ```  

---

### **🔹 Procesamiento con Spark**  
1. **Ejecutar script de procesamiento**  
   ```bash
   spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.0.5 spark_mongo_alpha.py
   ```  

---

## **📌 Visualización con Metabase**  
1. **Instalar Metabase**  
   ```bash
   sudo apt install openjdk-11-jdk -y
   mkdir ~/metabase && cd ~/metabase
   wget https://downloads.metabase.com/v0.46.3/metabase.jar
   java -jar metabase.jar
   ```  

2. **Acceder al dashboard**  
   ```
   http://<IP_PUBLICA_EC2>:3000
   ```  

---

## **📌 Automatización con Cron**  
1. **Programar ejecución automática**  
   ```bash
   crontab -e
   ```  
   Añadir:  
   ```bash
   0 * * * * /usr/bin/python3 /home/ubuntu/etf_proyecto/scripts/data_collection/descargar_alpha.py
   ```  


## **📌 Estructura del Repositorio**  
```
etf-sp500-bigdata-project/
├── docs/                          # Documentación
├── scripts/                       # Scripts Python
├── nifi_templates/                # Flujos de NiFi
├── sample_data/                   # Datos de ejemplo
├── images/                        # Imágenes
├── .env.template                  # Variables de entorno
├── requirements.txt               # Dependencias
└── README.md                      # Guía principal
```  


 


- Autores
  
  Ormeño Flores, Juan Julian
  
  Ordoñez Chuquihuaccha, Gerardo Angel
  
  Poviz Lazo, Leonel
  
  Rivas Tito, Frank Alex
  
  Vargas Estacio, Jesus Estacio
  
  

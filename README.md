# Documentación Técnica por Fases - Proyecto S&P 500 ETF

## Fase 1: Fuentes de Datos

### 1.1 Alpha Vantage API

- **Tipo**: Datos financieros históricos
- **Frecuencia**: Actualización diaria
- **Endpoint**: `TIME_SERIES_DAILY`
- **Datos recolectados**:
  ```json
  {
    "Meta Data": {
      "Symbol": "SPY",
      "Last Refreshed": "2025-06-28",
      "Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
      "2025-06-28": {
        "open": "420.15",
        "high": "422.30",
        "low": "418.75",
        "close": "421.80",
        "volume": "32015460"
      }
    }
  }

  ```

### 1.2 Twitter API v2

- **Filtros aplicados**:
  ```python
  query = '#SPY OR #S&P500 lang:es -is:retweet'
  tweet_fields = ['created_at', 'text', 'author_id', 'public_metrics']
  ```

### 1.3 Reddit API (PRAW)

- **Subreddits monitoreados**:
  ```python
  SUBREDDITS = ['stocks', 'investing', 'StockMarket']
  LIMIT = 200  # Máximo por subreddit
  ```

---

## Fase 2: Ingesta de Datos

### 2.1 Pipeline Apache NiFi

- **Flujo**:
  ```
  GetFile Alpha → PutMongo Alpha  
  GetFile Twitter → PutMongo Twitter  
  GetFile Reddit → PutMongo Reddit  
  ```
- **Configuraciones clave**:
  - Frecuencia de polling: 5 minutos
  - Rutas de entrada:
    - Financiero: `/etf_proyecto/data/alpha/`
    - Reddit: `/etf_proyecto/data/reddit/`
    - Twitter: `/etf_proyecto/data/twitter/`

### 2.2 Transformaciones Iniciales

- **Procesador**: `JoltTransformJSON`
  ```json
  {
    "operation": "shift",
    "spec": {
      "Time Series (Daily)": {
        "*": {
          "open": "[&1].open",
          "high": "[&1].high",
          "close": "[&1].close"
        }
      }
    }
  }
  ```

---

## Fase 3: Almacenamiento de Datos

### 3.1 Estructura MongoDB

- **Colección `alpha_raw`**:
  ```json
  {
    "_id": ObjectId("..."),
    "symbol": "SPY",
    "date": ISODate("2025-06-28"),
    "open": 420.15,
    "high": 422.30,
    "volume": 32015460
  }
  ```
- **Colección `reddit_processed`**:
  ```json
  {
    "post_id": "t3_xyz123",
    "content": "Análisis SPY Q3 2025",
    "engagement": {
      "score": 8421,
      "comments": 215
    },
    "source": "stocks"
  }
  ```

### 3.2 Índices Optimizados

```javascript
db.alpha_raw.createIndex({ symbol: 1, date: -1 })
db.twitter_processed.createIndex({ author_id: 1 })
db.reddit_processed.createIndex({ "engagement.score": -1 })
```

---

## Fase 4: Procesamiento y Análisis

### 4.1 Flujo Spark ETL

```python
def process_reddit(spark):
    df = spark.read.format("mongo").load()
    return df.withColumn(
        "date",
        from_unixtime(col("created_utc")).cast(DateType())
    ).filter(col("title").contains("SPY"))
```

### 4.2 Métricas Clave Calculadas

```sql
-- Correlación precio-volumen
SELECT
    date,
    close,
    volume,
    CORR(close, volume) OVER (ORDER BY date ROWS 7 PRECEDING) AS rolling_corr
FROM alpha_processed
```

---

## Fase 5: Visualización de Datos

### 5.1 Dashboard Metabase

- **Widget Precio SPY**:

  - Tipo: Serie temporal
  - Métrica: `close`
  - Filtro: Últimos 90 días
- **Heatmap Actividad Reddit**:

  ```sql
  SELECT
      HOUR(created_at) AS hour,
      DAYOFWEEK(created_at) AS day,
      COUNT(*) AS posts
  FROM reddit_processed
  GROUP BY hour, day
  ```

### 5.2 Plantilla de Visualización

```json
{
  "dashboard": {
    "name": "SPY Monitor",
    "cards": [
      {
        "type": "line",
        "title": "Precio de Cierre",
        "query": "SELECT date, close FROM alpha_processed..."
      }
    ]
  }
}
```

---

## Diagrama Final por Fases

```
Fuentes → API  
Ingesta → NiFi  
Almacenamiento → MongoDB  
Procesamiento → Spark  
Visualización → Metabase  
```

**Notas de Versión**:

- **v2.3**: 28/06/2025 - Estructura por fases validadas
- Autores
  
  Ormeño Flores, Juan Julian
  
  Ordoñez Chuquihuaccha, Gerardo Angel
  
  Poviz Lazo, Leonel
  
  Rivas Tito, Frank Alex
  
  Vargas Estacio, Jesus Estacio
  
  

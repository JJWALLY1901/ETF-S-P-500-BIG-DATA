import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

def download_alpha_data(symbol='SPY'):
    """Descarga datos diarios de Alpha Vantage para un símbolo dado"""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # Validar estructura de respuesta
        if 'Time Series (Daily)' not in data:
            raise ValueError("Formato de datos no válido")
        
        # Crear directorio si no existe
        os.makedirs('../data', exist_ok=True)
        
        # Guardar con marca de tiempo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"../data/{symbol}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"Datos guardados en {filename}")
        return filename
        
    except Exception as e:
        print(f"Error al descargar datos: {str(e)}")
        return None

if __name__ == "__main__":
    download_alpha_data('SPY')

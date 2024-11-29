# Paso 1: Instalar yfinance y pandas
# Primero abre la terminal y ejecuta los siguientes comandos para instalar las librerías necesarias:
# pip install yfinance pandas

import yfinance as yf
import json
import pandas as pd

# Lista inicial de ETFs en JSON
etfs_json = '''
[
    {"symbol": "CNYA", "name": "AZ China: ETF que invierte en empresas chinas"},
    {"symbol": "EWT", "name": "AZ MSCI TAIWAN INDEX FD: ETF que sigue el índice MSCI de Taiwán"},
    {"symbol": "IWM", "name": "AZ RUSSELL 2000: ETF que sigue el índice Russell 2000 de pequeñas empresas estadounidenses"},
    {"symbol": "EWZ", "name": "AZ Brasil: ETF que invierte en empresas brasileñas"},
    {"symbol": "EWU", "name": "AZ MSCI UNITED KINGDOM: ETF que sigue el índice MSCI del Reino Unido"},
    {"symbol": "XLF", "name": "AZ DJ US FINANCIAL SECT: ETF que sigue el sector financiero de EE.UU."},
    {"symbol": "BKF", "name": "AZ BRIC: ETF que invierte en los países BRIC (Brasil, Rusia, India, China)"},
    {"symbol": "EWY", "name": "AZ MSCI SOUTH KOREA IND: ETF que sigue el índice MSCI de Corea del Sur"},
    {"symbol": "AGG", "name": "AZ BARCLAYS AGGREGATE: ETF que invierte en bonos agregados de EE.UU."},
    {"symbol": "EEM", "name": "AZ Mercados Emergentes: ETF que invierte en mercados emergentes"},
    {"symbol": "EZU", "name": "AZ MSCI EMU: ETF que sigue el índice MSCI de la Unión Económica y Monetaria"},
    {"symbol": "FXI", "name": "AZ FTSE/XINHUA CHINA 25: ETF que invierte en las 25 principales empresas chinas"},
    {"symbol": "GLD", "name": "AZ Oro: ETF que sigue el precio del oro"},
    {"symbol": "QQQ", "name": "AZ QQQ NASDAQ 100: ETF que sigue el índice NASDAQ 100"},
    {"symbol": "AAXJ", "name": "AZ MSCI ASIA EX-JAPAN: ETF que sigue el índice MSCI de Asia excluyendo Japón"},
    {"symbol": "SHY", "name": "AZ BARCLAYS 1-3 YEAR TR: ETF que invierte en bonos del Tesoro de EE.UU. a corto plazo (1-3 años)"},
    {"symbol": "ACWI", "name": "AZ MSCI ACWI INDEX FUND: ETF que sigue el índice MSCI All Country World"},
    {"symbol": "SLV", "name": "AZ SILVER TRUST: ETF que sigue el precio de la plata"},
    {"symbol": "EWH", "name": "AZ MSCI HONG KONG INDEX: ETF que sigue el índice MSCI de Hong Kong"},
    {"symbol": "SPY", "name": "AZ SPDR S&P 500 ETF TRUST: ETF que sigue el índice S&P 500"},
    {"symbol": "EWJ", "name": "AZ MSCI JAPAN INDEX FD: ETF que sigue el índice MSCI de Japón"},
    {"symbol": "IEI", "name": "AZ BG EUR GOVT BOND 1-3: ETF que invierte en bonos gubernamentales de la Eurozona a corto plazo (1-3 años)"},
    {"symbol": "DIA", "name": "AZ SPDR DJIA TRUST: ETF que sigue el índice Dow Jones Industrial Average"},
    {"symbol": "EWQ", "name": "AZ MSCI FRANCE INDEX FD: ETF que sigue el índice MSCI de Francia"},
    {"symbol": "VWO", "name": "AZ VANGUARD EMERGING MARKET ETF: ETF que invierte en mercados emergentes globales"},
    {"symbol": "EWA", "name": "AZ MSCI AUSTRALIA INDEX: ETF que sigue el índice MSCI de Australia"},
    {"symbol": "XLF", "name": "AZ FINANCIAL SELECT SECTOR SPDR: ETF que sigue el sector financiero de EE.UU."},
    {"symbol": "EWC", "name": "AZ MSCI CANADA: ETF que sigue el índice MSCI de Canadá"},
    {"symbol": "ILF", "name": "AZ S&P LATIN AMERICA 40: ETF que sigue el índice S&P de las 40 principales empresas de América Latina"},
    {"symbol": "XLV", "name": "AZ HEALTH CARE SELECT SECTOR: ETF que sigue el sector salud de EE.UU."},
    {"symbol": "EWG", "name": "AZ MSCI GERMANY INDEX: ETF que sigue el índice MSCI de Alemania"},
    {"symbol": "ITB", "name": "AZ DJ US HOME CONSTRUCT: ETF que sigue el sector de la construcción de viviendas en EE.UU."}
]
'''

# Cargar JSON
etfs = json.loads(etfs_json)

# Función para verificar si el símbolo es válido en Yahoo Finance
def verify_etf_symbols(etfs):
    valid_etfs = []
    for etf in etfs:
        symbol = etf["symbol"]
        ticker = yf.Ticker(symbol)
        try:
            # Intentamos descargar un rango pequeño de datos para verificar si el símbolo es válido
            data = ticker.history(period="1d")
            if not data.empty:
                valid_etfs.append(etf)
                print(f"Valid symbol: {symbol} ({etf['name']})")
            else:
                print(f"Invalid symbol: {symbol} ({etf['name']})")
        except Exception as e:
            print(f"Error with symbol: {symbol} ({etf['name']}), Error: {str(e)}")
    
    return valid_etfs

# Verificar símbolos
valid_etfs = verify_etf_symbols(etfs)

# Guardar en un nuevo archivo JSON solo los símbolos válidos
with open('valid_etfs.json', 'w') as f:
    json.dump(valid_etfs, f, indent=4)

print("\nValid symbols saved to 'valid_etfs.json'")

# Paso 4: Ejecutar el script
# Una vez que hayas instalado las librerías necesarias, guarda este código en un archivo llamado 'verificar_etfs.py'.
# Luego, abre la terminal, navega hasta la carpeta donde guardaste el archivo y ejecuta:
# python verificar_etfs.py

import pandas as pd
import wbdata
from geopy.geocoders import Nominatim
from google.cloud import storage
from google.oauth2.service_account import Credentials
from io import StringIO

#  indicadores con los que definimos trabajar
indicadores = {
    "NY.GNP.PCAP.CD": "GNI per capita, Atlas method (current US$)",
    "SP.DYN.TFRT.IN": "Fertility rate, total (births per woman)",
    "SP.DYN.LE00.IN": "Life expectancy at birth, total (years)",
    "SH.DYN.MORT": "Mortality rate, under-5 (per 1,000 live births)",
    "SL.UEM.TOTL.ZS": "Unemployment, total (% of total labor force) (modeled ILO estimate)"
}
paises_latam_caribe = ['ATG', 'ARG', 'BHS', 'BRB', 'BLZ', 'BOL', 'BRA', 'CHL', 'COL',
                       'CRI', 'CUB', 'DMA', 'DOM', 'ECU', 'SLV', 'GRD', 'GTM', 'GUY',
                       'HTI', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'PRY', 'PER', 'PRI',
                       'KNA', 'LCA', 'VCT', 'SUR', 'TTO', 'URY', 'VEN']

# Descarga de indicadores para los países de América Latina y el Caribe
data = wbdata.get_dataframe(indicadores, country=paises_latam_caribe, convert_date=True)

data = data.reset_index()

data["date"] = data["date"].dt.year

df = data

while df[df['date']==df['date'].max()].isnull().sum(axis=1).sum()/len(df[df['date']==df['date'].max()]) > 2:
    df = df[df['date'] != df['date'].max()]

df_ultimos_30_anos = df.groupby('country').apply(lambda x: x.nlargest(30, 'date')).reset_index(drop=True)
data = df_ultimos_30_anos

data['country'] = data['country'].replace({'Bahamas, The': 'Bahamas' , 'Venezuela, RB': 'Venezuela'})
indicadores_latinoamerica = data
indicadores_latinoamerica.to_csv('indicadores_latinoamerica.csv')

paises_latinoamerica2 = ['Antigua and Barbuda', 'Argentina', 'Bolivia', 'Brazil', 'Belize', 'Bahamas', 'Barbados', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 
 'Dominican Republic', 'Dominica', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras', 'Jamaica', 'Mexico','Nicaragua', 'Panama', 'Paraguay',  
 'Peru', 'Puerto Rico', 'Suriname', 'St. Kitts and Nevis', 'St. Lucia', 'St. Vincent and the Grenadines', 'Trinidad and Tobago','Uruguay', 'Venezuela']

# Crear un geocodificador
geolocator = Nominatim(user_agent="my_app")

datos_geograficos = []

# Iterar sobre la lista de países
for pais in paises_latinoamerica2:
    try:
        # Geocodificar el país
        location = geolocator.geocode(pais)
        latitud = location.latitude
        longitud = location.longitude
        datos_geograficos.append({"País": pais, "Latitud": latitud, "Longitud": longitud})
    except:
        datos_geograficos.append({"País": pais, "Latitud": None, "Longitud": None})

# Crear un DataFrame con los datos geográficos
df_geografico = pd.DataFrame(datos_geograficos)
df_geografico.to_csv('df_geograficos.csv')


credentials_path = 'credentials.json'
credentials = Credentials.from_service_account_file(credentials_path)
client = storage.Client(credentials=credentials)

bucket_name = 'world_bank_data'
blob_name1 = 'indicadores_latinoamerica.csv' 
blob_name2 = 'df_geograficos.csv'  

bucket = client.get_bucket(bucket_name)
blob = bucket.blob(blob_name1)
blob.upload_from_filename('indicadores_latinoamerica.csv')

blob = bucket.blob(blob_name2)
blob.upload_from_filename('df_geograficos.csv')
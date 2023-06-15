import wbdata


# Definir los indicadores que deseas descargar
indicadores = {
    "NY.GNP.PCAP.CD": "GNI per capita, Atlas method (current US$)",
    "SP.DYN.TFRT.IN": "Fertility rate, total (births per woman)",
    "SP.DYN.LE00.IN": "Life expectancy at birth, total (years)",
    "SH.DYN.MORT": "Mortality rate, under-5 (per 1,000 live births)",
    "SL.UEM.TOTL.ZS": "Unemployment, total (% of total labor force) (modeled ILO estimate)"
}

# Definir los códigos de país de América Latina y el Caribe
paises_latam_caribe = ['ATG', 'ARG', 'BHS', 'BRB', 'BLZ', 'BOL', 'BRA', 'CHL', 'COL',
                       'CRI', 'CUB', 'DMA', 'DOM', 'ECU', 'SLV', 'GRD', 'GTM', 'GUY',
                       'HTI', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'PRY', 'PER', 'PRI',
                       'KNA', 'LCA', 'VCT', 'SUR', 'TTO', 'URY', 'VEN']

# Descargar los datos de los indicadores para los países de América Latina y el Caribe
data = wbdata.get_dataframe(indicadores, country=paises_latam_caribe, convert_date=True)

# Reiniciar los índices para convertir las columnas "country" y "date" en columnas regulares
data = data.reset_index()

# Filtrar los datos por los años 1990 a 2021
data = data.loc[(data['date'] >= '1990') & (data['date'] <= '2021')]

data["date"] = data["date"].dt.year

indicadores_latinoamerica = data
indicadores_latinoamerica.to_csv('indicadores_latinoamerica.csv')


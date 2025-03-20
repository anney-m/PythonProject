import pandas as pd
import geopandas as gpd # идея с использованием этой библиотеки и ее последующее освоение происходило с помощью нейросетей

moscow_districts = gpd.read_file('export.geojson')
fitness_centers_df = pd.read_excel('fitness_centers_moscow_with_address.xlsx')

coordinates = fitness_centers_df['Координаты'].str.split(',', expand=True)
fitness_centers_df['lat'] = coordinates[0].astype(float)
fitness_centers_df['lon'] = coordinates[1].astype(float)

points = []
for i in range(len(fitness_centers_df)):
    lon = fitness_centers_df['lon'][i]
    lat = fitness_centers_df['lat'][i]
    points.append((lon, lat))

fitness_centers_gdf = gpd.GeoDataFrame(
    fitness_centers_df,
    geometry=gpd.points_from_xy(fitness_centers_df['lon'], fitness_centers_df['lat'])
)

# настройка координат
fitness_centers_gdf.crs = moscow_districts.crs

# для каждого зала находим, в каком районе он находится и добавляем в датафрейм
districts = []
for i in range(len(fitness_centers_gdf)):
    point = fitness_centers_gdf['geometry'][i]
    district_name = None
    for j in range(len(moscow_districts)):
        if moscow_districts['geometry'][j].contains(point):
            district_name = moscow_districts['name'][j]
            break
    districts.append(district_name)

fitness_centers_gdf['district'] = districts

# подсчет количества залов в каждом районе, чтобы выбрать, где ниша свободна
district_counts = fitness_centers_gdf['district'].value_counts()

min_count = district_counts.min()
min_districts = district_counts[district_counts == min_count]

print("Районы с минимальным количеством фитнес-клубов:")
print(min_districts)
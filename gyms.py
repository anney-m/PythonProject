import requests
import pandas as pd

api_key = ''
url = 'https://catalog.api.2gis.ru/3.0/items'

lat_min, lat_max = 55.0840, 56.0217
lon_min, lon_max = 36.8015, 37.9678

grid_size = 50

fitness_centers = []

lat_step = (lat_max - lat_min) / grid_size
lon_step = (lon_max - lon_min) / grid_size

for i in range(grid_size):
    for j in range(grid_size):
        point1_lat = lat_max - i * lat_step
        point1_lon = lon_min + j * lon_step
        point2_lat = lat_max - (i + 1) * lat_step
        point2_lon = lon_min + (j + 1) * lon_step

        params = {
            'key': api_key,
            'q': 'Москва фитнес клуб',
            'fields': "items.point, items.name, items.address_name, items.address_comment",
            # Добавлено поле address_name
            'point1': f'{point1_lon},{point1_lat}',
            'point2': f'{point2_lon},{point2_lat}',
            'page_size': 10
        }

        print(f"Запрос для области {i + 1},{j + 1}: {point1_lat}, {point1_lon} -> {point2_lat}, {point2_lon}")

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'items' in data['result']:
                items = data['result']['items']
                print(f"Получено {len(items)} элементов для области {i + 1},{j + 1}")

                if items:
                    for item in items:
                        lat = item.get("point", {}).get("lat")
                        lon = item.get("point", {}).get("lon")
                        if lat is None or lon is None:
                            coord_str = "Нет данных"
                        else:
                            coord_str = f"{lat}, {lon}"
                        address_name = item.get('address_name', 'Нет данных')
                        address_comment = item.get('address_comment', '')
                        address = f"{address_name}, {address_comment}".strip(', ')

                        fitness_centers.append({
                            'Название': item.get('name', 'Неизвестно'),
                            'Адрес': address,
                            'Координаты': coord_str
                        })
                else:
                    print(f"Нет данных в ответе для области {i + 1},{j + 1}")
            else:
                print(f"Ответ не содержит ожидаемых данных для области {i + 1},{j + 1}")
        else:
            print(f"Ошибка на области {i + 1},{j + 1}: {response.status_code}, Сообщение: {response.text}")

if fitness_centers:
    df = pd.DataFrame(fitness_centers)
    df.to_excel('fitness_centers_moscow_with_address.xlsx', index=False)
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

# Функция для очистки цен
def clean_price(price_str):
    # Удаляем пробелы и нечисловые символы, кроме точки
    cleaned_price = re.sub(r'[^\d.]', '', price_str)
    return float(cleaned_price) if cleaned_price else 0.0

# Спарсим первый сайт
url = "https://wsstudio.info/tseny/"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

price_items = soup.find_all('span', class_='elementor-price-list-price')
services_items = soup.find_all('span', class_='elementor-price-list-title')

services = []
prices = []

fetched_items = list(zip(services_items, price_items))

for fetched_service, fetched_price in fetched_items:
    services.append(fetched_service.text.strip())
    prices.append(fetched_price.text.split('₽')[0])

first_website = pd.DataFrame({
    'Название услуги': services,
    'Цена': prices
})

print(prices)

first_website['Цена'] = first_website['Цена'].apply(clean_price)

with pd.ExcelWriter('services_data1.xlsx') as writer:
    first_website.to_excel(writer, sheet_name='Services', index=False)

# Спарсим второй сайт
url = "https://moyfit.com/?ysclid=m8c5kffnqy385506837#rec778251736"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

price_items = soup.find_all('div', class_='t1072__price t-title t-title_xs')
services_items = soup.find_all('div', class_='t-card__title t-name t-name_md')
membership_items = soup.find_all('div', class_='t-card__title t-name t-name_lg')

services = []
prices = []
memberships = []

fetched_items = list(zip(membership_items, price_items))

for fetched_membership, fetched_price in fetched_items:
    memberships.append(fetched_membership.text.strip())
    prices.append(fetched_price.text.replace(".", ""))

for service in services_items:
    services.append(service.text.strip())

second_website = pd.DataFrame({
    'Вид абонемента': memberships,
    'Цена': prices
})

second_website_services = pd.DataFrame({
    'Название услуги': services,
})

second_website['Цена'] = second_website['Цена'].apply(clean_price)

with pd.ExcelWriter('services_data2.xlsx') as writer:
    second_website.to_excel(writer, sheet_name='Memberships', index=False)
    second_website_services.to_excel(writer, sheet_name='Services', index=False)

# Спарсим третий сайт
url = "https://reshape.global/price#accord10"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
buttons = soup.find_all('a', class_='tn-atom')

result = []
used_buttons = set()

for button in buttons:
    if button.text == '+':
        continue
    button_text = button.text.strip()
    related_texts = []
    prices = []
    name = None
    processed_ids = set()

    for elem in button.find_all_previous(class_='tn-atom'):
        parent = elem.find_parent('div', class_='tn-elem')

        if parent and parent.has_attr('data-elem-id'):
            if parent['class'][-1] in used_buttons:
                continue
            used_buttons.add(parent['class'][-1])
            elem_id = parent['data-elem-id']

            if parent.get('data-elem-type') == 'text':
                text = elem.text.strip()
                if 'Бесконечно много часов тренировок в любое время суток' in text:
                    continue
                if 'Тренировки на РЕФОРМЕРАХ проходят на Парке Культуры' in text:
                    continue
                if 'Индивидуальные тренировкиЛЮБОЕ ВРЕМЯ' in text:
                    continue
                if '₽' in text and not '*' in text:
                    # Разделяем строку на отдельные цены
                    prices.extend([p.strip() for p in text.split('₽') if p.strip()])
                    continue
                if text == text.upper():
                    name = text
                    continue

                if '+' in text or '%' in text or '*' in text or 'без заморозки' in text or 'Для тренировок до 16:00и по выходным' in text:
                    continue
                if text:
                    related_texts.append(text)

    related_texts.reverse()
    prices.reverse()

    if name:
        result.append({
            'name': name,
            'prices': prices,
            'related_texts': related_texts
        })
    
    
url = "https://reshape.global/"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
services_items = soup.find_all('div', class_='t-card__title t-name t-name_md')
services = [service.text.strip() for service in services_items]
lists = []

with pd.ExcelWriter('services_data3.xlsx', engine='openpyxl') as writer:
    if result:
        for item in result:
            name = item['name']
            related_texts = item['related_texts']
            prices = item['prices']

            sheet_name = re.sub(r'[\\/*?:\[\]]', '', name)[:31]

            third_website = pd.DataFrame({
                'Вид абонемента': related_texts,
                'Цены': prices
            })

            third_website['Цены'] = third_website['Цены'].apply(lambda x: clean_price(x) if isinstance(x, str) else x)
            lists.append(third_website)          
            third_website.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        print("Нет данных о ценах и абонементах.")

    if services:
        third_website_services = pd.DataFrame({
            'Название услуги': services,
        })
        third_website_services.to_excel(writer, sheet_name='Услуги', index=False)
    else:
        print("Нет данных о названиях услуг.")

third_website = pd.concat(lists, ignore_index=True)

# Дашборды
# Я решила оформить дашборд в одной цветовой гамме,
# и нейросеть любезно подсказала мне, какие конкретно html кода цветов мне нужны и как их добавить в мой проект
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

first_website_mean = first_website['Цена'].mean()
second_website_mean = second_website['Цена'].mean()
third_website_mean = third_website['Цены'].mean()

data = {
    'Фитнес-зал': ['Women Secrets', 'Мой фитнес', 'Reshape'],
    'Средняя цена': [first_website_mean, second_website_mean, third_website_mean]
}

df_for_dashboard = pd.DataFrame(data)

fig = px.bar(df_for_dashboard, x='Фитнес-зал', y='Средняя цена', color='Фитнес-зал', color_discrete_sequence=['#FF69B4', '#FF1493', '#DB7093'])
fig.update_layout(
    title_text='Средняя цена услуги у конкурентов',
    title_x=0.5,
    title_font_size=30,
    plot_bgcolor='#FFF0F5',
    paper_bgcolor='#FFF0F5'
)

text_card = dbc.Card(
    [
        dbc.CardHeader(
            'Информация о данных',
            style={
                'fontSize': '24px',
                'fontWeight': 'bold',
                'backgroundColor': '#FF69B4',
                'color': 'white'
            }
        ),
        dbc.CardBody(
            [
                html.P(
                    'Получили три датасета с услугами конкурентов.',
                    style={'fontSize': '18px', 'color': '#333333'}
                ),
                html.P(
                    'Данные включают цены, виды тренировок и абонементов.',
                    style={'fontSize': '18px', 'color': '#333333'}
                )
            ],
            style={'backgroundColor': '#FFF0F5'}  # Розовый фон тела карточки
        )
    ]
)

dropdown_style = {'backgroundColor': '#FFF0F5', 'color': '#333333'}
card_style = {'backgroundColor': '#FFF0F5', 'border': '1px solid #FF69B4'}

dropdown_first = dcc.Dropdown(
    id='dropdown-first',
    options=[{'label': service, 'value': service} for service in first_website['Название услуги']],
    value=first_website['Название услуги'][0],
    style=dropdown_style
)

dropdown_second = dcc.Dropdown(
    id='dropdown-second',
    options=[{'label': service, 'value': service} for service in second_website_services['Название услуги']],
    value=second_website_services['Название услуги'][0],
    style=dropdown_style
)

dropdown_third = dcc.Dropdown(
    id='dropdown-third',
    options=[{'label': service, 'value': service} for service in third_website_services['Название услуги']],
    value=third_website_services['Название услуги'][0],
    style=dropdown_style
)

card_first = dbc.Card(
    [
        dbc.CardHeader('Women Secrets', style={'backgroundColor': '#FF69B4', 'color': 'white'}),
        dbc.CardBody(
            [
                html.P('Виды тренировок и прочих услуг', style={'color': '#333333'}),
                dropdown_first
            ],
            style=card_style
        )
    ]
)

card_second = dbc.Card(
    [
        dbc.CardHeader('Мой фитнес', style={'backgroundColor': '#FF69B4', 'color': 'white'}),
        dbc.CardBody(
            [
                html.P('Виды тренировок и прочих услуг', style={'color': '#333333'}),
                dropdown_second
            ],
            style=card_style
        )
    ]
)

card_third = dbc.Card(
    [
        dbc.CardHeader('Reshape', style={'backgroundColor': '#FF69B4', 'color': 'white'}),
        dbc.CardBody(
            [
                html.P('Виды тренировок и прочих услуг', style={'color': '#333333'}),
                dropdown_third
            ],
            style=card_style
        )
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H1("Анализ конкурентов", style={'color': '#FF69B4'}), align='stretch')
            ]
        ),
        dbc.Row(
            [
                dbc.Col(card_first, md=6, lg=4),
                dbc.Col(card_second, md=6, lg=4),
                dbc.Col(card_third, md=12, lg=4),
            ],
            align='center'
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig), md=12)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(text_card, md=12)
            ]
        )
    ],
    style={'backgroundColor': '#FFF0F5'}
)

if __name__ == '__main__':
    app.run(debug=True)



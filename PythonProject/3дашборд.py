import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('1bars.csv', encoding='utf-8-sig')
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Анализ протеиновых батончиков REX", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Выберите категорию:"),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in df['Категория'].unique()],
            value=df['Категория'].unique()[0],
            clearable=False
        ),
        html.Label("Выберите диапазон калорий:"),
        dcc.RangeSlider(
            id='kcal-slider',
            min=df['Ккал'].min(),
            max=df['Ккал'].max(),
            step=10,
            marks={i: str(i) for i in range(int(df['Ккал'].min()), int(df['Ккал'].max()) + 2, 50)},
            value=[df['Ккал'].min(), df['Ккал'].max()]
        )
    ], style={'margin': '20px'}),

    dcc.Graph(id='nutrition-graph'),
    html.Div([
        html.H3("Таблица данных"),
        html.Div(id='data-table')
    ], style={'margin': '20px'})
])
@app.callback(
    [Output('nutrition-graph', 'figure'),
     Output('data-table', 'children')],
    [Input('category-dropdown', 'value'),
     Input('kcal-slider', 'value')]
)
def update_dashboard(selected_category, kcal_range):
    filtered_df = df[(df['Категория'] == selected_category) &
                     (df['Ккал'] >= kcal_range[0]) &
                     (df['Ккал'] <= kcal_range[1])]

    print("Отфильтрованные данные:")
    print(filtered_df)
    fig = px.bar(filtered_df, x='Вкус', y=['Белки (г)', 'Жиры (г)', 'Углеводы (г)'],
                 barmode='group', title=f'Пищевая ценность ({selected_category})')

    table = html.Table(
        [html.Thead(html.Tr([html.Th(col) for col in filtered_df.columns]))] +
        [html.Tbody([html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns])
         for i in range(len(filtered_df))]
    )])

    return fig, table

if __name__ == '__main__':
    app.run(debug=True)
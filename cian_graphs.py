import pandas as pd
import plotly.express as px

df = pd.read_excel("cian_data.xlsx")

# числовые данные в эксель были сохранены в текстовом формате, нужно отформатировать, потом перевести в числа, чтобы строить графики
df["Цена (руб/мес)"] = df["Цена (руб/мес)"].astype(str)
df["Цена (руб/мес)"] = df["Цена (руб/мес)"].str.replace(',', '.', regex=True)
df["Цена (руб/мес)"] = df["Цена (руб/мес)"].str.replace('\xa0', '', regex=True)  # здесь помог Chat GPT, рассказал, что можно добавить удаление неразрывных пробелов, regex=True, чтобы избежать ошибок и неккоректную интерпретацию символов

df["Площадь (м²)"] = df["Площадь (м²)"].astype(str)
df["Площадь (м²)"] = df["Площадь (м²)"].str.replace(',', '.', regex=True)
df["Площадь (м²)"] = df["Площадь (м²)"].str.replace('\xa0', '', regex=True)

df["Цена (руб/мес)"] = pd.to_numeric(df["Цена (руб/мес)"], errors='coerce')
df["Площадь (м²)"] = pd.to_numeric(df["Площадь (м²)"], errors='coerce')

df = df.dropna(subset=["Площадь (м²)", "Цена (руб/мес)"])

df["Номер помещения"] = range(1, len(df) + 1)

# 1
fig1 = px.bar(df, x="Номер помещения", y="Цена (руб/мес)", title="Цены на выбранные помещения", text="Цена (руб/мес)")
fig1.update_traces(textposition='outside', marker_color='deeppink')
fig1.update_layout(xaxis_title="Номер помещения", yaxis_title="Цена (руб/мес)", showlegend=False,plot_bgcolor='lavenderblush',
    paper_bgcolor='lavenderblush')
fig1.show()

# 2
fig2 = px.bar(df, x="Номер помещения", y="Площадь (м²)", title="Площади помещений", text="Площадь (м²)")
fig2.update_traces(textposition='outside', marker_color='deeppink')
fig2.update_layout(xaxis_title="Номер помещения", yaxis_title="Площадь (м²)", showlegend=False, plot_bgcolor='lavenderblush',
    paper_bgcolor='lavenderblush')
fig2.show()

# добавляем новый столбец в датафрейм - цена за квадратный метр
df["Цена за м²"] = df["Цена (руб/мес)"] / df["Площадь (м²)"]
# 3
fig3 = px.scatter(df, x="Номер помещения", y="Цена за м²", title="Соотношение цен и площадей каждого помещения", text="Цена за м²")
fig3.update_traces(textposition='top center',marker_color='deeppink')
fig3.update_layout(xaxis_title="Номер помещения", yaxis_title="Цена за м² (руб/м²)", showlegend=False, plot_bgcolor='lavenderblush',
    paper_bgcolor='lavenderblush')
fig3.show()
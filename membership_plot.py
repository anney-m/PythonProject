import pandas as pd
import matplotlib.pyplot as plt


def extract_months(df):
    months = []
    for item in df['Вид абонемента']:
        if 'месяц' in item:
            months.append(int(item.split()[0]))
    return months

def plot_min_max_months(ax, title, months, color):
    min_months = min(months)
    max_months = max(months)

    ax.bar(['Минимальное', 'Максимальное'], [min_months, max_months], color=color)
    ax.set_ylabel('Количество месяцев')
    ax.set_title(title)
    ax.set_facecolor('#FFF0F5')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#FF69B4')
    ax.spines['bottom'].set_color('#FF69B4')
    ax.tick_params(axis='x', colors='#FF69B4')
    ax.tick_params(axis='y', colors='#FF69B4')


data2 = pd.read_excel('services_data2.xlsx', sheet_name='Memberships')
months2 = extract_months(data2)

data3 = pd.read_excel('services_data3.xlsx', sheet_name='ЛЮБОЕ ВРЕМЯ')
months3 = extract_months(data3)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='#FFF0F5')
fig.suptitle('Минимальное и максимальное количество месяцев в абонементах', fontsize=16, color='#FF69B4')

plot_min_max_months(ax1, 'Мой фитнес', months2, '#FF69B4')
plot_min_max_months(ax2, 'Reshape', months3, '#FF1493')

plt.tight_layout()
plt.savefig('month_plot.png', dpi=300, bbox_inches='tight', facecolor='#FFF0F5')
plt.show()

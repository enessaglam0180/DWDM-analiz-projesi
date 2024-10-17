import pandas as pd
import plotly.express as px
import webbrowser

# DWDM_analiz.xlsx dosyasını yükleme
df = pd.read_excel('DWDM_analiz.xlsx')

# Tarih sütununu datetime formatına çevirme (eğer değilse)
df['Date'] = pd.to_datetime(df['Date'])

# Veriyi tarih ve Shelf/Slot numarası ile sıralama
df_sorted = df.sort_values(by=['Shelf/Slot', 'Date'])

# Grafik oluşturma
fig = px.scatter(
    df_sorted,
    x='Date',
    y='Shelf/Slot',
    color='Card Type',
    symbol='Card Type',
    hover_data={
        'Date': True,
        'Shelf/Slot': True,
        'Card Type': True,
        'Çalışma Süresi (Gün)': True
    },
    labels={
        'Date': 'Tarih',
        'Shelf/Slot': 'Shelf/Slot Numarası',
        'Card Type': 'Kart Tipi',
        'Çalışma Süresi (Gün)': 'Çalışma Süresi (Gün)'
    },
    title='Shelf/Slot Numaralarında Kart Tipi Değişimleri'
)

# Grafik düzenlemeleri
fig.update_layout(
    xaxis_title='Tarih',
    yaxis_title='Shelf/Slot Numarası',
    legend_title='Kart Tipi',
    xaxis=dict(
        tickformat='%Y-%m-%d',
        tickangle=45
    ),
    hovermode='closest'
)

# Zaman ekseninde çizgiler ekleme (kart tipi değişimlerini daha net göstermek için)
fig.update_traces(mode='markers+lines', connectgaps=True)

# Grafik HTML dosyasına kaydetme
html_file = 'kart_tipi_degisimi_grafik.html'
fig.write_html(html_file)

# HTML dosyasını tarayıcıda açma
webbrowser.open(html_file)

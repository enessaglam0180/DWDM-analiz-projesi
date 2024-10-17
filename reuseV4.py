import pandas as pd
import plotly.express as px
import webbrowser

# DWDM_analiz.xlsx dosyasını yükleme
df = pd.read_excel('DWDM_analiz.xlsx')

# Veriyi tarih ve Shelf/Slot numarası ile sıralama
df_sorted = df.sort_values(by=['Date', 'Shelf/Slot'])

# Grafik oluşturma
fig = px.scatter(
    df_sorted,
    x='Date',
    y='Shelf/Slot',
    size='Çalışma Süresi (Gün)',
    color='Shelf/Slot',
    hover_name='Shelf/Slot',
    hover_data={'Date': True, 'Çalışma Süresi (Gün)': True},
    labels={'Date': 'Tarih', 'Shelf/Slot': 'Shelf/Slot Numara', 'Çalışma Süresi (Gün)': 'Çalışma Süresi (Gün)'},
    title='Çalışma Sürelerinin Zaman İçindeki Dağılımı'
)

# Grafik başlığı ve eksen etiketlerini ekleme
fig.update_layout(
    xaxis_title='Tarih',
    yaxis_title='Shelf/Slot Numara',
    xaxis=dict(
        tickformat='%Y-%m-%d'
    )
)

# Grafik HTML dosyasına kaydetme
html_file = 'grafik.html'
fig.write_html(html_file)

# HTML dosyasını tarayıcıda açma
webbrowser.open(html_file)

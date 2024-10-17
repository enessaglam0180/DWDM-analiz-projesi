import pandas as pd
import plotly.express as px
import webbrowser

# DWDM_analiz.xlsx dosyasını yükleme
df = pd.read_excel('DWDM_analiz.xlsx')

# Veriyi tarih, Card Type ve Shelf/Slot numarası ile sıralama
df_sorted = df.sort_values(by=['Date', 'Shelf/Slot'])

# Grafik oluşturma
fig = px.scatter(
    df_sorted,
    x='Date',
    y='Card Type',  # y ekseninde Card Type kullanılıyor
    size='Çalışma Süresi (Gün)',
    color='Shelf/Slot',  # Renkler Shelf/Slot numarasına göre
    hover_name='Shelf/Slot',
    hover_data={
        'Date': True,
        'Çalışma Süresi (Gün)': True,
        'Shelf/Slot': True,
        'Card Type': True  # Hover'da Card Type bilgisi de gösterilecek
    },
    labels={
        'Date': 'Tarih',
        'Shelf/Slot': 'Shelf/Slot Numara',
        'Çalışma Süresi (Gün)': 'Çalışma Süresi (Gün)',
        'Card Type': 'Kart Tipi'
    },
    title='Çalışma Sürelerinin Zaman İçindeki Dağılımı'
)

# Grafik başlığı ve eksen etiketlerini ekleme
fig.update_layout(
    xaxis_title='Tarih',
    yaxis_title='Kart Tipi',  # Y ekseni etiketi Card Type olarak ayarlandı
    xaxis=dict(
        tickformat='%Y-%m-%d'
    )
)

# Grafik HTML dosyasına kaydetme
html_file = 'grafik.html'
fig.write_html(html_file)

# HTML dosyasını tarayıcıda açma
webbrowser.open(html_file)

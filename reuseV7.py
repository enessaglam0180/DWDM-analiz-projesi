import pandas as pd
import plotly.express as px

# Veriyi yükleme
df = pd.read_excel('DWDM_analiz.xlsx')

# Tarih sütununu datetime formatına çevirme (eğer değilse)
df['Date'] = pd.to_datetime(df['Date'])

# Kart değişim sayısını hesaplama
df['Kart Değişim Sayısı'] = df.groupby(['Shelf/Slot', 'Card Type'])['Date'].transform('count')

# Kartın ilk takıldığı tarih ve son değiştirildiği tarih arasındaki farkı hesaplama (gün cinsinden)
df['Kartın Yaşı (Gün)'] = df.groupby(['Shelf/Slot', 'Card Type'])['Date'].transform(lambda x: (x.max() - x.min()).days)

# Her kart tipi için ortalama yaş ve değişim sayısını hesaplama
df_summary = df.groupby('Card Type').agg(
    Ortalama_Yas=('Kartın Yaşı (Gün)', 'mean'),
    Degisim_Sayisi=('Kart Değişim Sayısı', 'mean')
).reset_index()

# Analiz sonuçlarını görselleştirme
fig = px.scatter(
    df_summary,
    x='Ortalama_Yas',
    y='Degisim_Sayisi',
    text='Card Type',
    size='Degisim_Sayisi',
    title='Kart Yaşı ve Değişim Sayısı Arasındaki İlişki',
    labels={
        'Ortalama_Yas': 'Ortalama Kart Yaşı (Gün)',
        'Degisim_Sayisi': 'Ortalama Kart Değişim Sayısı'
    }
)

# Grafik düzenlemeleri
fig.update_traces(textposition='top center')
fig.update_layout(
    xaxis_title='Ortalama Kart Yaşı (Gün)',
    yaxis_title='Ortalama Kart Değişim Sayısı'
)

# Grafik gösterimi
fig.show()

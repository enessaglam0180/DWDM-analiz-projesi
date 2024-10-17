import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser

# Veriyi yükle
df = pd.read_excel('DWDM_analiz.xlsx')
df['Date'] = pd.to_datetime(df['Date'])

# Veriyi hazırla
df['DaysSinceStart'] = (df['Date'] - df['Date'].min()).dt.days
df['PreviousCardType'] = df.groupby('Shelf/Slot')['Card Type'].shift(1)
df['CardChanged'] = (df['Card Type'] != df['PreviousCardType']).astype(int)

# Kategori değişkenlerini sayısallaştır
le = LabelEncoder()
df['CardTypeEncoded'] = le.fit_transform(df['Card Type'])
df['ShelfSlotEncoded'] = le.fit_transform(df['Shelf/Slot'])

# Özellikler ve hedef değişkeni ayarla
X = df[['DaysSinceStart', 'CardTypeEncoded', 'ShelfSlotEncoded', 'Çalışma Süresi (Gün)']]
y = df['CardChanged']

# Veriyi eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli eğit
model = LogisticRegression()
model.fit(X_train, y_train)

# Test seti üzerinde tahminler yap
df['PredictedChange'] = model.predict(X)

# Grafik oluştur
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=('Kart Tipi Değişimleri', 'Değişim Tahminleri'))

# Üst grafik: Gerçek değişimler
fig.add_trace(
    go.Scatter(x=df['Date'], y=df['Shelf/Slot'], mode='markers',
               marker=dict(color=df['CardTypeEncoded'], colorscale='Viridis'),
               text=df['Card Type'], hoverinfo='text+x+y',
               name='Gerçek Kart Tipi'),
    row=1, col=1
)

# Alt grafik: Tahmin edilen değişimler
fig.add_trace(
    go.Scatter(x=df['Date'], y=df['Shelf/Slot'], mode='markers',
               marker=dict(color=df['PredictedChange'], colorscale='RdYlGn',
                           symbol='square', size=8),
               text=['Değişim' if p else 'Değişim Yok' for p in df['PredictedChange']],
               hoverinfo='text+x+y',
               name='Tahmin Edilen Değişim'),
    row=2, col=1
)

# Grafik düzenlemeleri
fig.update_layout(height=800, title_text="Kart Değişimleri ve Tahminleri")
fig.update_xaxes(title_text="Tarih", row=2, col=1)
fig.update_yaxes(title_text="Shelf/Slot Numarası", row=1, col=1)
fig.update_yaxes(title_text="Shelf/Slot Numarası", row=2, col=1)

# HTML dosyasına kaydet ve aç
html_file = 'kart_degisimi_tahminleri.html'
fig.write_html(html_file)
webbrowser.open(html_file)

# Model performansını yazdır
print(f"Model Doğruluğu: {model.score(X_test, y_test):.2f}")
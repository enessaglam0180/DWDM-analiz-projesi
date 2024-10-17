import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser

# Load the data
df = pd.read_excel('DWDM_analiz.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df_sorted = df.sort_values(by=['Shelf/Slot', 'Date'])

# Create the main scatter plot
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

# Update traces
fig.update_traces(mode='markers+lines', connectgaps=True)

# Create a range slider
range_slider = go.layout.XAxis(
    rangeslider=dict(visible=True),
    type="date"
)

# Update layout
fig.update_layout(
    xaxis=range_slider,
    xaxis_title='Tarih',
    yaxis_title='Shelf/Slot Numarası',
    legend_title='Kart Tipi',
    hovermode='closest'
)

# Save and open the HTML file
html_file = 'kart_tipi_degisimi_grafik_enhanced.html'
fig.write_html(html_file)
webbrowser.open(html_file)
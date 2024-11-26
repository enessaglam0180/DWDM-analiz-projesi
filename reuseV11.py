import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as sns  
from scipy import stats  
import statsmodels.api as sm  

# Veriyi yükle  
df = pd.read_excel('DWDM_analiz.xlsx')  
df['Date'] = pd.to_datetime(df['Date'])  

# Her Shelf/Slot için kart değişim sayısını hesapla  
card_changes = df.groupby('Shelf/Slot').agg({  
    'Card Type': lambda x: (x != x.shift()).sum(),  
    'Date': ['min', 'max']  
})  
card_changes.columns = ['Changes', 'Start_Date', 'End_Date']  
card_changes['Duration'] = (card_changes['End_Date'] - card_changes['Start_Date']).dt.days  

# Aykırı değerleri kontrol et  
plt.figure(figsize=(12, 6))  
sns.boxplot(x=card_changes['Duration'])  
plt.title('Kullanım Süresi Aykırı Değer Kontrolü')  
plt.xlabel('Kullanım Süresi (gün)')  
plt.show()  

# Korelasyon analizi  
correlation = stats.pearsonr(card_changes['Duration'], card_changes['Changes'])  

# Görselleştirme  
plt.figure(figsize=(12, 6))  
sns.scatterplot(data=card_changes, x='Duration', y='Changes', alpha=0.7)  
plt.title('Shelf/Slot Kullanım Süresi vs Kart Değişim Sayısı')  
plt.xlabel('Kullanım Süresi (gün)')  
plt.ylabel('Kart Değişim Sayısı')  

# Regresyon çizgisi ekle  
sns.regplot(data=card_changes, x='Duration', y='Changes', scatter=False, color='red')  

plt.text(0.05, 0.95, f'Korelasyon: {correlation[0]:.2f}\np-değeri: {correlation[1]:.4f}',   
         transform=plt.gca().transAxes, verticalalignment='top')  

plt.tight_layout()  
plt.show()  

# Kart tiplerine göre ortalama kullanım süresi  
card_type_duration = df.groupby('Card Type').agg({  
    'Çalışma Süresi (Gün)': 'mean'  
}).sort_values('Çalışma Süresi (Gün)', ascending=False)  

# Ortalama kullanım süresi görselleştirme  
plt.figure(figsize=(12, 6))  
sns.barplot(data=card_type_duration.reset_index(), x='Card Type', y='Çalışma Süresi (Gün)')  
plt.title('Kart Tiplerine Göre Ortalama Kullanım Süresi')  
plt.xticks(rotation=45, ha='right')  
plt.tight_layout()  
plt.show()  

print(card_type_duration)  

# Zaman içinde kart değişim oranı  
df['YearMonth'] = df['Date'].dt.to_period('M')  
changes_over_time = df.groupby('YearMonth').agg({  
    'Card Type': lambda x: (x != x.shift()).sum(),  
    'Shelf/Slot': 'count'  
}).reset_index()  
changes_over_time['Change_Rate'] = changes_over_time['Card Type'] / changes_over_time['Shelf/Slot']  

# Zaman içinde kart değişim oranı görselleştirme  
plt.figure(figsize=(12, 6))  
plt.plot(changes_over_time['YearMonth'].dt.to_timestamp(), changes_over_time['Change_Rate'])  
plt.title('Zaman İçinde Aylık Kart Değişim Oranı')  
plt.xlabel('Tarih')  
plt.ylabel('Değişim Oranı')  
plt.xticks(rotation=45, ha='right')  
plt.tight_layout()  
plt.show()  

print(changes_over_time)  

# Regresyon analizi  
X = sm.add_constant(card_changes['Duration'])  # Sabit terimi ekle  
model = sm.OLS(card_changes['Changes'], X).fit()  
print(model.summary())
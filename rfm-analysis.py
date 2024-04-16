# RFM Metriklerinin hesaplanması:

# Recency, Frequency, Monetary

# Bugünün tarihini belirleyelim
today_date = dt.datetime(2010, 12, 11)
type(today_date)  # today_date değişkeninin veri tipini kontrol edelim. (datetime olmalı)

# RFM metriklerini hesaplayalım
rfm = df.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda r: (today_date - order_purchase_timestamp.max()).days,  # Recency hesaplaması
    'order_id': lambda f: order_id.nunique(),  # Frequency hesaplaması
    'payment_value': lambda m: payment_value.sum()  # Monetary hesaplaması
})

rfm.columns = ['recency', 'frequency', 'monetary']

# RFM metriklerinin istatistiksel özeti
rfm.describe().T

# Monetary değeri sıfırdan büyük olan gözlemleri seçelim
rfm = rfm[rfm["monetary"] > 0]

# Veri setinin boyutunu kontrol edelim
rfm.shape

###############################################################
# RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################

# Recency skorunu hesaplayalım
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

# Frequency skorunu hesaplayalım
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]) 

# Monetary skorunu hesaplayalım
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

# RFM skorunu oluşturalım
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

# RFM skorlarının istatistiksel özetini alalım
rfm.describe().T

# RFM skoru 55 olan müşterileri filtreleyelim
rfm[rfm["RFM_SCORE"] == "55"]

# RFM skoru 11 olan müşterileri filtreleyelim
rfm[rfm["RFM_SCORE"] == "11"]

# RFM skoru 33 olan müşterileri filtreleyelim
rfm[rfm["RFM_SCORE"] == "33"]

# RFM segmentlerini belirleyelim
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

# RFM segmentlerini belirleyelim ve "segment" adında yeni bir sütun oluşturalım
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

# Her segment için ortalama recency, frequency ve monetary değerlerini ve gözlem sayısını hesaplayalım
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

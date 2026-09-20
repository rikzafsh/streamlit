import pandas as pd
import streamlit as st
import altair as alt
from transformers import pipeline

# Load model pretrained IndoBERT khusus klasifikasi sentimen
@st.cache_resource
def load_sentiment_pipeline():
    model_name = "mdhugol/indonesia-bert-sentiment-classification"
    return pipeline("sentiment-analysis", model=model_name)

# Function untuk analisis sentimen per kata (token)
def analyze_token_sentiment(docx, sentiment_pipeline):
    pos_list = []
    neg_list = []
    neu_list = []
    
    words = docx.split()
    for word in words:
        if len(word.strip()) > 1:  # Abaikan tanda baca/karakter tunggal
            res = sentiment_pipeline(word)[0]
            label = res['label']
            score = round(res['score'], 4)
            
            if label == "LABEL_0":  # Positif
                pos_list.extend([word, score])
            elif label == "LABEL_2":  # Negatif
                neg_list.extend([word, score])
            else:  # Netral (LABEL_1)
                neu_list.append(word)
                
    return {'positives': pos_list, 'negatives': neg_list, 'neutral': neu_list}

def main():
    st.title("Analisis Sentimen Teks Bahasa Indonesia")
    st.subheader("Streamlit Projects")
    
    sentiment_pipeline = load_sentiment_pipeline()
    
    with st.form("nlpForm_indo"):
        raw_text = st.text_area("Masukkan teks/kalimat Bahasa Indonesia:")
        submit_button = st.form_submit_button(label='Analyze')
        
    if submit_button and raw_text.strip() != "":
        # Layout 2 Kolom (Sesuai modul)
        col1, col2 = st.columns(2)
        
        # Prediksi Sentimen Teks Utama
        result = sentiment_pipeline(raw_text)[0]
        top_label = result['label']
        confidence_val = round(result['score'], 4)
        
        label_map = {
            "LABEL_0": ("Positive", "😃", confidence_val),
            "LABEL_1": ("Neutral", "😐", 0.0),
            "LABEL_2": ("Negative", "😡", -abs(confidence_val))
        }
        
        sentiment_label, emoji, polarity_val = label_map.get(
            top_label, ("Neutral", "😐", 0.0)
        )

        # ---------------- KOLOM 1: Results ----------------
        with col1:
            st.info("Results")
            
            # 1. Output JSON dasar
            raw_result = {
                "polarity": polarity_val,
                "subjectivity": confidence_val
            }
            st.write(raw_result)
            
            # 2. Status Sentiment & Emoji
            st.markdown(f"Sentiment:: {sentiment_label} {emoji}")
            
            # 3. Dataframe
            metrics_data = [
                {'metric': 'polarity', 'value': polarity_val},
                {'metric': 'subjectivity', 'value': confidence_val}
            ]
            result_df = pd.DataFrame(metrics_data)
            st.dataframe(result_df)
            
            # 4. Chart Altair
            c = alt.Chart(result_df).mark_bar().encode(
                x='metric',
                y='value',
                color='metric'
            )
            st.altair_chart(c, use_container_width=True)

        # ---------------- KOLOM 2: Token Sentiment ----------------
        with col2:
            st.info("Token Sentiment")
            token_sentiments = analyze_token_sentiment(raw_text, sentiment_pipeline)
            st.write(token_sentiments)

if __name__ == "__main__":
    main()
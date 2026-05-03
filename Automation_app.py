import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Civil 3D Automation", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.stButton>button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50px;
    padding: 12px 30px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Civil 3D Automation Pro")
st.markdown("### Upload your survey file (CSV, Excel, TXT)")

uploaded_file = st.file_uploader("📁 Upload Survey File", type=['csv', 'xls', 'xlsx', 'txt'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file, sep=None, engine='python')

        if 'X' in df.columns and 'Y' in df.columns and 'Z' in df.columns:
            df['Status'] = 'Processed'
            df['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output_file = f'processed_batch_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            df.to_csv(output_file, index=False)

            st.success("✅ Processing Complete!")
            st.dataframe(df)
            st.download_button("📥 Download Results", df.to_csv(index=False), output_file, "text/csv")
        else:
            st.error("❌ File must contain X, Y, Z columns")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

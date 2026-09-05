import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
import datetime
import time
import traceback

# ==========================================
# 1. إعدادات الصفحة والثيم (Google Finance)
# ==========================================
try:
    st.set_page_config(page_title="SamaKarbala Finance", layout="wide", initial_sidebar_state="collapsed")
except Exception:
    pass

st.markdown("""
    <style>
        /* ثيم Google Finance */
        .stApp { background-color: #202124 !important; color: #e8eaed !important; direction: rtl; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; }
        
        /* الكروت الإحصائية */
        div[data-testid="metric-container"] {
            background-color: #292a2d !important; border: 1px solid #3c4043 !important; padding: 15px !important; border-radius: 8px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
        }
        div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 2.2rem !important; font-weight: 500 !important; }
        div[data-testid="stMetricLabel"] { color: #9aa0a6 !important; font-size: 0.95rem !important; }
        div[data-testid="stMetricDelta"] > div { font-size: 0.9rem !important; }
        
        /* إخفاء القوائم الافتراضية */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* التابات (الأقسام) */
        div.row-widget.stRadio > div {
            display: flex; flex-direction: row; justify-content: center; gap: 20px;
            background-color: #202124; padding: 10px 0; border-bottom: 1px solid #3c4043; flex-wrap: wrap; margin-bottom: 20px;
        }
        div.stRadio > div[role="radiogroup"] > label {
            background-color: transparent !important; border: none !important; padding: 8px 0 !important; border-radius: 0 !important;
            cursor: pointer !important; box-shadow: none !important; border-bottom: 2px solid transparent !important;
        }
        div.stRadio > div[role="radiogroup"] > label > div:first-child { display: none !important; }
        div.stRadio > div[role="radiogroup"] > label:hover p { color: #8ab4f8 !important; }
        div.stRadio > div[role="radiogroup"] > label[data-checked="true"] { border-bottom: 2px solid #8ab4f8 !important; }
        div.stRadio > div[role="radiogroup"] > label[data-checked="true"] p { color: #8ab4f8 !important; font-weight: bold !important; }
        div.stRadio > div[role="radiogroup"] > label p { color: #e8eaed !important; font-size: 1rem !important; margin: 0; }

        /* الجداول (Dataframes) والـ Expanders */
        [data-testid="stDataFrame"] { background-color: #292a2d; border-radius: 8px; border: 1px solid #3c4043; }
        div[data-testid="stExpander"] { background-color: #292a2d !important; border-radius: 8px; border: 1px solid #3c4043; margin-bottom: 15px; }
        div[data-testid="stExpander"] summary { color: #e8eaed !important; font-weight: 500; }
        
        /* الفلاتر */
        div[data-baseweb="select"] > div, input { border-radius: 4px !important; background-color: #303134 !important; border: 1px solid #5f6368 !important; color: #e8eaed !important; }
        div[data-baseweb="select"] > div:hover, input:hover { border-color: #8ab4f8 !important; }
        
        /* أزرار التطبيق */
        div[data-testid="stFormSubmitButton"] > button, .stButton > button {
            background-color: #8ab4f8 !important; color: #202124 !important; border: none; border-radius: 4px !important; font-weight: 600; height: 45px;
        }
        div[data-testid="stFormSubmitButton"] > button:hover, .stButton > button:hover { background-color: #aecbfa !important; }

        /* العناوين */
        h1, h2, h3 { color: #e8eaed !important; font-weight: 400 !important; }
        .finance-title { color: #8ab4f8; font-weight: bold; }
        hr { border-top: 1px solid #3c4043 !important; margin-top: 1.5rem; margin-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

gf_layout = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#9aa0a6'),
    xaxis=dict(showgrid=False, gridcolor='#3c4043', zeroline=False),
    yaxis=dict(showgrid=True, gridcolor='#3c4043', zeroline=False),
    margin=dict(t=40, b=10, l=10, r=10)
)
gf_colors = ['#8ab4f8', '#81c995', '#f28b82', '#fde293', '#c58af9', '#f48fb1', '#78d9ec']

# ==========================================
# 2. الهيدر وزر التحديث
# ==========================================
col_title, col_btn = st.columns([5, 1])
with col_title:
    st.markdown("<h1><span class='finance-title'>Finance</span> SamaKarbala</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #81c995; font-size: 0.85rem; margin-top: -10px;'>السوق متصل • التحديث الأخير: {datetime.datetime.now().strftime('%H:%M UTC')}</p>", unsafe_allow_html=True)
with col_btn:
    st.write("") 
    if st.button("تحديث البيانات 🔄", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# ==========================================
# 3. شريط التابات الكامل (7 أقسام)
# ==========================================
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'gov'

tabs_dict = {
    "📍 المحافظات": "gov",
    "🧊 الثلاجات": "frz",
    "❄️ مخازن المجزر": "slh",
    "📊 عام المجزر": "slh_gen",
    "📦 المواد الأولية": "mat",
    "🛒 مشتريات المصنفات": "pur_cat",
    "🔪 مشتريات المجزر": "pur_slh"
}

choice = st.radio("القوائم", list(tabs_dict.keys()), horizontal=True, label_visibility="collapsed")
st.session_state.active_tab = tabs_dict[choice]

# ==========================================
# 4. دوال السحب المضادة للتعليق (Robust Fetch)
# ==========================================
def fetch_sheet_csv(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    for _ in range(3):
        try:
            # كسر الكاش لضمان جلب أحدث داتا
            final_url = url + ('&' if '?' in url else '?') + 't=' + str(time.time())
            res = requests.get(final_url, headers=headers, timeout=15)
            if res.status_code == 200:
                res.encoding = 'utf-8'
                df = pd.read_csv(io.StringIO(res.text), on_bad_lines='skip')
                if not df.empty:
                    df.columns = [str(c).replace('\ufeff', '').strip() for c in df.columns]
                    return df
        except Exception:
            pass
        time.sleep(1)
    # محاولة أخيرة بـ pandas مباشرة
    try:
        df = pd.read_csv(url, on_bad_lines='skip')
        df.columns = [str(c).replace('\ufeff', '').strip() for c in df.columns]
        return df
    except Exception:
        return pd.DataFrame()

# دالة مساعدة لرسم التحليلات المخصصة
def custom_analysis_lab(df, cat_cols, num_cols, key_prefix):
    st.markdown("### مختبر التحليلات المخصص")
    with st.form(f"form_{key_prefix}"):
        ca1, ca2 = st.columns(2)
        x_axis = ca1.selectbox("محور المقارنة (X):", cat_cols) if cat_cols else None
        y_axis = ca2.selectbox("القيم (Y):", num_cols) if num_cols else None
        submitted = st.form_submit_button("رسم التحليل 📊")
    if submitted and x_axis and y_axis:
        try:
            custom_df = df.groupby(x_axis)[y_axis].sum().reset_index().sort_values(by=y_axis, ascending=False).head(15)
            fig = px.bar(custom_df, x=x_axis, y=y_axis, title=f"تحليل {y_axis} حسب {x_axis}")
            fig.update_traces(marker_color='#8ab4f8')
            fig.update_layout(**gf_layout)
            st.plotly_chart(fig, use_container_width=True)
        except Exception: pass

# ==========================================
# 5. دوال تحميل البيانات لكل قسم
# ==========================================
@st.cache_data(ttl=300)
def load_gov_data():
    df = fetch_sheet_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRdYYKBv1JCC2q5pcgJAc6QyQGJc9Lsz9EaPD8t2HC5KADIoVzkFCJ-6JaF4tbdfw/pub?output=csv")
    if df.empty: return df, None, None, None, None, None, None, None, None, None
    c_date = next((c for c in df.columns if 'تاريخ' in c or 'date' in c.lower()), None)
    c_gov = next((c for c in df.columns if 'محافظ' in c), None)
    c_agent = next((c for c in df.columns if 'زبون' in c or 'وكيل' in c), None)
    c_item = next((c for c in df.columns if 'مادة' in c or 'product' in c.lower()), None)
    c_cat = 'Category' if 'Category' in df.columns else next((c for c in df.columns if 'تصنيف' in c), None)
    c_ff = next((c for c in df.columns if 'item type' in c.lower() or 'طازج' in c or 'fresh' in c.lower()), None)
    c_label = next((c for c in df.columns if 'own' in c.lower() or 'label' in c.lower()), None)
    c_ton = next((c for c in df.columns if 'طن' in c), None)
    c_qty = next((c for c in df.columns if 'عدد' in c), None)
    if c_date: df[c_date] = pd.to_datetime(df[c_date], errors='coerce')
    for c in [c_ton, c_qty]:
        if c and c in df.columns: df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d\.-]', '', regex=True), errors='coerce').fillna(0)
    for c in [c_gov, c_agent, c_item, c_cat, c_ff, c_label]:
        if c and c in df.columns: df[c] = df[c].fillna('غير مصنف')
    return df, c_date, c_gov, c_agent, c_item, c_cat, c_ff, c_label, c_ton, c_qty

@st.cache_data(ttl=300)
def load_freezer_data():
    df = fetch_sheet_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQDphmbL58bqGdSFFFpU7NfVtAefvztGcjf5zPX8FBl5Rj3tW6H8vySo3T8CXGzyQ/pub?output=csv")
    if df.empty: return df, None, None, None, None, None, None, None
    c_item = next((c for c in df.columns if 'ماد' in c), None)
    c_frz = next((c for c in df.columns if 'ثلاج' in c), None)
    c_start = next((c for c in df.columns if 'رصيد' in c), None)
    c_prod = next((c for c in df.columns if 'نتاج' in c), None)
    c_sold = next((c for c in df.columns if 'مباع' in c or 'صادر' in c), None)
    c_short = next((c for c in df.columns if 'نقص' in c), None)
    c_final = next((c for c in df.columns if 'نهائي' in c), None)
    for c in [c_start, c_prod, c_sold, c_short, c_final]:
        if c and c in df.columns: df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d\.-]', '', regex=True), errors='coerce').fillna(0)
    if c_item: df[c_item] = df[c_item].fillna('غير مصنف')
    if c_frz: df[c_frz] = df[c_frz].fillna('غير مصنف')
    return df, c_item, c_frz, c_start, c_prod, c_sold, c_short, c_final

@st.cache_data(ttl=300)
def load_slh_data():
    df = fetch_sheet_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQHSv4SF_rudpU2753hjWpkwyuiQ59RHr3zfiZZb43IOmdf1PZvytibN_Dc5Oxwxg/pub?output=csv")
    if df.empty: return df, None, None, None, None, None, None, None
    c_date = next((c for c in df.columns if 'Date' in str(c) or 'تاريخ' in str(c)), None)
    c_qty = next((c for c in df.columns if 'Qty' in str(c) or 'كمية' in str(c)), None)
    c_prev = next((c for c in df.columns if 'Previous' in str(c) or 'رصيد' in str(c)), None)
    c_prod = next((c for c in df.columns if 'Production' in str(c) or 'إنتاج' in str(c)), None)
    c_sold = next((c for c in df.columns if 'Sold' in str(c) or 'مباع' in str(c)), None)
    c_item = next((c for c in df.columns if 'Item Name' in str(c) or 'المادة' in str(c)), None)
    c_code = next((c for c in df.columns if 'Code' in str(c) or 'كود' in str(c)), None)
    if c_date: df[c_date] = pd.to_datetime(df[c_date], errors='coerce')
    for c in [c_qty, c_prev, c_prod, c_sold]:
        if c and c in df.columns: df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d\.-]', '', regex=True), errors='coerce').fillna(0)
    if c_item: df[c_item] = df[c_item].fillna('غير مصنف')
    return df, c_date, c_qty, c_prev, c_prod, c_sold, c_item, c_code

@st.cache_data(ttl=300)
def load_slh_gen_data():
    df = fetch_sheet_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTiM4ycja48KN-96D91Ppv0CHRkIzyOBGgpAszLcOEID09N5CYspJSSsU98wvIFyQ/pub?output=csv")
    if df.empty: return df, None, None, None, None, None, None, None, None, None
    c_cat = next((c for c in df.columns if 'تصنيف' in c), None)
    c_item = next((c for c in df.columns if 'مادة' in c), None)
    c_unit = next((c for c in df.columns if 'وحدة' in c), None)
    c_bal = next((c for c in df.columns if 'الرصيد' in c and '/' not in c and '+' not in c), None)
    c_confirmed = next((c for c in df.columns if 'المثبت' in c and '/' not in c and '+' not in c and 'مطلوب' not in c), None)
    c_total_bal = next((c for c in df.columns if 'الرصيد' in c and 'المثبت' in c and '/' not in c), None)
    c_req = next((c for c in df.columns if 'مطلوب' in c), None)
    c_forecast = next((c for c in df.columns if 'فوركاست' in c), None)
    c_coverage = next((c for c in df.columns if 'يكفي' in c and '+' not in c), None)
    for c in [c_bal, c_confirmed, c_total_bal, c_req, c_forecast, c_coverage]:
        if c and c in df.columns: df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d\.-]', '', regex=True), errors='coerce').fillna(0)
    for c in [c_cat, c_item, c_unit]:
        if c and c in df.columns: df[c] = df[c].fillna('غير محدد')
    return df, c_cat, c_item, c_unit, c_bal, c_confirmed, c_total_bal, c_req, c_forecast, c_coverage

@st.cache_data(ttl=300)
def load_mat_data():
    df = fetch_sheet_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTyT8AIVzoC083IILST_hw5Q4j29tMBoYpdA568JyzSuJuOnX0BKq0MwOa9GE0aBQ/pub?output=csv")
    if df.empty: return df, None, None, None, None, None, None, None
    
    # معالجة الهيدر المعقد
    cols_str = ' '.join(df.columns.astype(str))
    if 'المادة' not in cols_str and 'الكمية' not in cols_str:
        header_idx = None
        for idx, row in df.head(15).iterrows():
            row_str = ' '.join(str(val) for val in row.values)
            if 'المادة' in row_str or 'الكمية' in row_str or 'تاريخ' in row_str:
                header_idx = idx; break
        if header_idx is not None:
            df.columns = df.iloc[header_idx]
            df = df.iloc[header_idx + 1:].reset_index(drop=True)
            df.columns = [str(c).replace('\ufeff', '').strip() for c in df.columns]

    c_date = next((c for c in df.columns if 'تاريخ' in c), None)
    c_type = next((c for c in df.columns if 'نوع' in c), None)
    c_dept = next((c for c in df.columns if 'قسم' in c), None)
    c_item = next((c for c in df.columns if 'مادة' in c and 'كود' not in c), None)
    c_qty = next((c for c in df.columns if 'كمية' in c), None)
    c_bal = next((c for c in df.columns if 'رصيد' in c and 'حالي' in c), None)
    c_cat = next((c for c in df.columns if 'تصنيف' in c), None)
    
    for c in [c_qty, c_bal]:
        if c and c in df.columns: df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d\.-]', '', regex=True).replace('-', '0'), errors='coerce').fillna(0)
    if c_date: df[c_date] = pd.to_datetime(df[c_date], errors='coerce')
    return df, c_date, c_type, c_dept, c_item, c_qty, c_bal, c_cat

@st.cache_data(ttl=300)
def load_pur_cat_data():
    df = fetch_sheet_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSQ5lFKwIUSMCyYxRvpRMUl3PDlO6JY-x07zi0FgH9O2Atbryh4TjEpH7UGxtQ_Cw/pub?output=csv")
    if df.empty: return df, None, None, None, None, None, None, None, None
    c_emp = next((c for c in df.columns if 'الموظف' in c), None)
    c_arr = next((c for c in df.columns if 'وصول' in c), None)
    c_ord_date = next((c for c in df.columns if 'تاريخ الطلب' in c), None)
    c_comp = next((c for c in df.columns if 'الشركة' in c), None)
    c_req = next((c for c in df.columns if 'المطلوب' in c), None)
    c_cur = next((c for c in df.columns if 'الرصيد' in c), None)
    c_unit = next((c for c in df.columns if 'الوحدة' in c), None)
    c_item = next((c for c in df.columns if 'اسم المادة' in c or 'المادة' in c), None)
    for c in [c_req, c_cur]:
        if c and c in df.columns: df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d\.-]', '', regex=True), errors='coerce').fillna(0)
    if c_ord_date: df[c_ord_date] = pd.to_datetime(df[c_ord_date], errors='coerce', dayfirst=True)
    return df, c_emp, c_arr, c_ord_date, c_comp, c_req, c_cur, c_unit, c_item

@st.cache_data(ttl=300)
def load_pur_slh_data():
    df = fetch_sheet_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRfd4_W6y4OJ_Ztbn9d1oJwFz9JOpgyExrOjdnG8Y5ecBDZZctHbo-099vM6-5tdw/pub?output=csv")
    if df.empty: return df, None, None, None, None, None, None, None, None, None, None
    c_code = next((c for c in df.columns if 'كود' in c or 'Code' in c), None)
    c_item = next((c for c in df.columns if 'المادة' in c), None)
    c_cat = next((c for c in df.columns if 'تصنيف' in c), None)
    c_dept = next((c for c in df.columns if 'القسم' in c), None)
    c_unit = next((c for c in df.columns if 'الوحدة' in c), None)
    c_cur = next((c for c in df.columns if 'الرصيد' in c), None)
    c_req = next((c for c in df.columns if 'المطلوب' in c), None)
    c_comp = next((c for c in df.columns if 'الشركة' in c or 'شركة' in c), None)
    c_date = next((c for c in df.columns if 'تاريخ' in c), None)
    c_status = next((c for c in df.columns if 'حالة' in c or 'توقيت' in c), None)
    
    for c in [c_req, c_cur]:
        if c and c in df.columns: df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d\.-]', '', regex=True), errors='coerce').fillna(0)
    if c_date: df[c_date] = pd.to_datetime(df[c_date], errors='coerce', dayfirst=True)
    for c in [c_comp, c_status, c_item, c_cat]:
        if c and c in df.columns: df[c] = df[c].fillna('غير محدد')
        
    return df, c_code, c_item, c_cat, c_dept, c_unit, c_cur, c_req, c_comp, c_date, c_status

# ==========================================
# 6. العرض حسب القسم المختار
# ==========================================

# ----------------- 1. المحافظات -----------------
if st.session_state.active_tab == 'gov':
    df_gov, c_date, c_gov, c_agent, c_item, c_cat, c_ff, c_label, c_ton, c_qty = load_gov_data()
    if not df_gov.empty:
        with st.expander("🔍 فلاتر المبيعات", expanded=True):
            with st.form("gov_form"):
                f1, f2, f3, f4 = st.columns(4)
                if c_date:
                    valid_dates = df_gov[c_date].dropna()
                    if not valid_dates.empty:
                        min_d, max_d = valid_dates.min().date(), valid_dates.max().date()
                        use_date = f1.checkbox("تفعيل فلتر التاريخ")
                        date_range = f1.date_input("الفترة", [min_d, max_d], min_value=min_d, max_value=max_d) if use_date else []
                sel_gov = f2.multiselect("المحافظة", df_gov[c_gov].unique() if c_gov else [])
                sel_ff = f3.multiselect("طازج/مجمد", df_gov[c_ff].unique() if c_ff else [])
                sel_label = f4.multiselect("العلامة", df_gov[c_label].unique() if c_label else [])
                submit_gov = st.form_submit_button("تطبيق הפلاتر")
                
        df_f = df_gov.copy()
        if 'use_date' in locals() and use_date and len(date_range) == 2 and c_date:
            df_f = df_f[(df_f[c_date].dt.date >= date_range[0]) & (df_f[c_date].dt.date <= date_range[1])]
        if sel_gov: df_f = df_f[df_f[c_gov].isin(sel_gov)]
        if sel_ff: df_f = df_f[df_f[c_ff].isin(sel_ff)]
        if sel_label: df_f = df_f[df_f[c_label].isin(sel_label)]

        st.markdown("<br>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("إجمالي المبيعات (طن)", f"{df_f[c_ton].sum():,.2f}" if c_ton else "0")
        k2.metric("إجمالي المبيعات (صندوق)", f"{df_f[c_qty].sum():,.0f}" if c_qty else "0")
        k3.metric("وكلاء وزبائن", f"{df_f[c_agent].nunique()}" if c_agent else "0")
        k4.metric("السجلات المسجلة", f"{len(df_f)}")
        st.markdown("---")

        if c_cat and c_ton and c_gov:
            p1, p2, p3 = st.columns(3)
            with p1:
                fig = px.pie(df_f.groupby(c_cat)[c_ton].sum().reset_index(), values=c_ton, names=c_cat, title="التصنيف", color_discrete_sequence=gf_colors, hole=0.5)
                fig.update_layout(**gf_layout)
                st.plotly_chart(fig, use_container_width=True)
            with p2:
                fig = px.pie(df_f.groupby(c_ff)[c_ton].sum().reset_index(), values=c_ton, names=c_ff, title="طازج / مجمد", color_discrete_sequence=['#8ab4f8', '#81c995'], hole=0.5)
                fig.update_layout(**gf_layout)
                st.plotly_chart(fig, use_container_width=True)
            with p3:
                fig = px.pie(df_f.groupby(c_label)[c_ton].sum().reset_index(), values=c_ton, names=c_label, title="العلامة التجارية", color_discrete_sequence=['#fde293', '#f28b82'], hole=0.5)
                fig.update_layout(**gf_layout)
                st.plotly_chart(fig, use_container_width=True)
                
            fig_gov = px.bar(df_f.groupby(c_gov)[c_ton].sum().reset_index().sort_values(by=c_ton), x=c_ton, y=c_gov, orientation='h', title="توزيع المحافظات")
            fig_gov.update_traces(marker_color='#8ab4f8')
            fig_gov.update_layout(**gf_layout, height=400)
            st.plotly_chart(fig_gov, use_container_width=True)

        st.markdown("---")
        custom_analysis_lab(df_f, [c for c in [c_gov, c_agent, c_item, c_cat, c_ff, c_label] if c], [c for c in [c_ton, c_qty] if c], "gov")
        st.markdown("---")
        with st.expander("قاعدة البيانات الأساسية (Raw Data)"):
            st.dataframe(df_f, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات. اضغط تحديث.")

# ----------------- 2. الثلاجات -----------------
elif st.session_state.active_tab == 'frz':
    df_frz, c_item, c_frz, c_start, c_prod, c_sold, c_short, c_final = load_freezer_data()
    if not df_frz.empty:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("المخزون الفعلي (Current)", f"{df_frz[c_final].sum():,.0f}" if c_final else "0")
        k2.metric("حجم الإنتاج (Prod)", f"{df_frz[c_prod].sum():,.0f}" if c_prod else "0")
        k3.metric("إجمالي المباع (Sold)", f"{df_frz[c_sold].sum():,.0f}" if c_sold else "0")
        k4.metric("النقص والتالف (Shortage)", f"{df_frz[c_short].sum():,.0f}" if c_short else "0")
        st.markdown("---")

        if c_frz and c_final:
            r1, r2 = st.columns(2)
            with r1:
                fig = px.bar(df_frz.groupby(c_frz)[c_final].sum().reset_index().sort_values(by=c_final), x=c_frz, y=c_final, title="الأرصدة الحالية في الثلاجات")
                fig.update_traces(marker_color='#8ab4f8')
                fig.update_layout(**gf_layout)
                st.plotly_chart(fig, use_container_width=True)
            with r2:
                short_df = df_frz.groupby(c_frz)[c_short].sum().reset_index()
                if short_df[c_short].sum() > 0:
                    fig = px.pie(short_df, values=c_short, names=c_frz, title="توزيع النقص والتالف", hole=0.5, color_discrete_sequence=['#f28b82'])
                    fig.update_layout(**gf_layout)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.success("✅ لا يوجد نقص مسجل في الثلاجات")
                    
        st.markdown("---")
        custom_analysis_lab(df_frz, [c for c in [c_item, c_frz] if c], [c for c in [c_start, c_prod, c_sold, c_short, c_final] if c], "frz")
        st.markdown("---")
        with st.expander("قاعدة بيانات الثلاجات (Raw Data)"):
            st.dataframe(df_frz, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات. اضغط تحديث.")

# ----------------- 3. مخازن المجزر -----------------
elif st.session_state.active_tab == 'slh':
    df_slh, c_date, c_qty, c_prev, c_prod, c_sold, c_item, c_code = load_slh_data()
    if not df_slh.empty:
        with st.expander("🔍 فلاتر المجزر", expanded=True):
            with st.form("slh_form"):
                f1, f2 = st.columns(2)
                sel_item = f1.multiselect("المادة", df_slh[c_item].unique() if c_item else [])
                submit_slh = st.form_submit_button("تطبيق הפلاتر")
        
        df_f = df_slh.copy()
        if sel_item: df_f = df_f[df_f[c_item].isin(sel_item)]

        st.markdown("<br>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("إجمالي الكمية (Qty)", f"{df_f[c_qty].sum():,.0f}" if c_qty else "0")
        k2.metric("حجم الإنتاج (Prod)", f"{df_f[c_prod].sum():,.0f}" if c_prod else "0")
        k3.metric("إجمالي المباع (Sold)", f"{df_f[c_sold].sum():,.0f}" if c_sold else "0")
        k4.metric("الأرصدة السابقة (Prev)", f"{df_f[c_prev].sum():,.0f}" if c_prev else "0")
        st.markdown("---")

        if c_item and c_qty:
            r1, r2 = st.columns(2)
            with r1:
                pie_df = pd.DataFrame({'العملية': ['الإنتاج', 'المباع'], 'الكمية': [df_f[c_prod].sum() if c_prod else 0, df_f[c_sold].sum() if c_sold else 0]})
                fig = px.pie(pie_df, values='الكمية', names='العملية', title="الإنتاج مقابل المبيعات", hole=0.5, color_discrete_sequence=['#8ab4f8', '#f28b82'])
                fig.update_layout(**gf_layout)
                st.plotly_chart(fig, use_container_width=True)
            with r2:
                fig = px.bar(df_f.groupby(c_item)[c_qty].sum().reset_index().nlargest(10, c_qty).sort_values(by=c_qty), x=c_qty, y=c_item, orientation='h', title="أعلى المواد توفراً")
                fig.update_traces(marker_color='#81c995')
                fig.update_layout(**gf_layout)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        custom_analysis_lab(df_f, [c for c in [c_item, c_code] if c], [c for c in [c_qty, c_prev, c_prod, c_sold] if c], "slh")
        st.markdown("---")
        with st.expander("قاعدة بيانات المجزر (Raw Data)"):
            st.dataframe(df_f, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات. اضغط تحديث.")

# ----------------- 4. عام المجزر -----------------
elif st.session_state.active_tab == 'slh_gen':
    df_gen, c_cat, c_item, c_unit, c_bal, c_confirmed, c_total_bal, c_req, c_forecast, c_coverage = load_slh_gen_data()
    if not df_gen.empty:
        with st.expander("🔍 فلاتر عام المجزر (Forecasting)", expanded=True):
            with st.form("gen_form"):
                f1, f2 = st.columns(2)
                sel_cat = f1.multiselect("التصنيف", df_gen[c_cat].unique() if c_cat else [])
                sel_item = f2.multiselect("المادة", df_gen[c_item].unique() if c_item else [])
                submit_gen = st.form_submit_button("تطبيق הפلاتر")
        
        df_f = df_gen.copy()
        if sel_cat: df_f = df_f[df_f[c_cat].isin(sel_cat)]
        if sel_item: df_f = df_f[df_f[c_item].isin(sel_item)]

        st.markdown("<br>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("إجمالي الرصيد الفعلي", f"{df_f[c_bal].sum():,.0f}" if c_bal else "0")
        k2.metric("المثبت (قيد الوصول)", f"{df_f[c_confirmed].sum():,.0f}" if c_confirmed else "0")
        k3.metric("المطلوب تثبيته", f"{df_f[c_req].sum():,.0f}" if c_req else "0")
        crit_count = len(df_f[(df_f[c_coverage] < 7) & (df_f[c_coverage] > 0)]) if c_coverage else 0
        k4.metric("مواد بخطر (< 7 أيام)", str(crit_count))
        st.markdown("---")

        if c_item and c_bal and c_confirmed:
            top_15 = df_f.nlargest(15, c_bal)
            melted = top_15.melt(id_vars=c_item, value_vars=[c_bal, c_confirmed], var_name='النوع', value_name='الكمية')
            fig = px.bar(melted, x=c_item, y='الكمية', color='النوع', barmode='group', title="الرصيد الفعلي مقابل المثبت", color_discrete_map={c_bal: '#8ab4f8', c_confirmed: '#81c995'})
            fig.update_layout(**gf_layout, xaxis_title="", legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        custom_analysis_lab(df_f, [c for c in [c_cat, c_item, c_unit] if c], [c for c in [c_bal, c_confirmed, c_total_bal, c_req, c_forecast, c_coverage] if c], "slh_gen")
        st.markdown("---")
        with st.expander("قاعدة البيانات الشاملة (Raw Data)"):
            st.dataframe(df_f, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات. اضغط تحديث.")

# ----------------- 5. المواد الأولية -----------------
elif st.session_state.active_tab == 'mat':
    df_mat, c_date, c_type, c_dept, c_item, c_qty, c_bal, c_cat = load_mat_data()
    if not df_mat.empty:
        with st.expander("🔍 فلاتر المواد", expanded=True):
            with st.form("mat_form"):
                f1, f2 = st.columns(2)
                sel_dept = f1.multiselect("القسم", df_mat[c_dept].unique() if c_dept else [])
                sel_cat = f2.multiselect("التصنيف", df_mat[c_cat].unique() if c_cat else [])
                submit_mat = st.form_submit_button("تطبيق הפلاتر")
        
        df_f = df_mat.copy()
        if sel_dept: df_f = df_f[df_f[c_dept].isin(sel_dept)]
        if sel_cat: df_f = df_f[df_f[c_cat].isin(sel_cat)]

        st.markdown("<br>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("إجمالي الرصيد الحالي", f"{df_f[c_bal].sum():,.0f}" if c_bal else "0")
        k2.metric("حركة الكميات", f"{df_f[c_qty].sum():,.0f}" if c_qty else "0")
        k3.metric("الأقسام النشطة", f"{df_f[c_dept].nunique()}" if c_dept else "0")
        k4.metric("السجلات المسجلة", f"{len(df_f)}")
        st.markdown("---")

        if c_dept and c_bal:
            r1, r2 = st.columns(2)
            with r1:
                fig = px.bar(df_f.groupby(c_dept)[c_bal].sum().reset_index().sort_values(by=c_bal), x=c_bal, y=c_dept, orientation='h', title="أرصدة الأقسام")
                fig.update_traces(marker_color='#8ab4f8')
                fig.update_layout(**gf_layout)
                st.plotly_chart(fig, use_container_width=True)
            with r2:
                fig = px.pie(df_f.groupby(c_cat)[c_bal].sum().reset_index(), values=c_bal, names=c_cat, title="توزيع الأصناف", hole=0.5, color_discrete_sequence=gf_colors)
                fig.update_layout(**gf_layout)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        custom_analysis_lab(df_f, [c for c in [c_dept, c_type, c_cat, c_item] if c], [c for c in [c_qty, c_bal] if c], "mat")
        st.markdown("---")
        with st.expander("قاعدة بيانات المواد (Raw Data)"):
            st.dataframe(df_f, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات. اضغط تحديث.")

# ----------------- 6. مشتريات المصنفات -----------------
elif st.session_state.active_tab == 'pur_cat':
    df_pur_cat, c_emp, c_arr, c_ord_date, c_comp, c_req, c_cur, c_unit, c_item = load_pur_cat_data()
    if not df_pur_cat.empty:
        with st.expander("🔍 فلاتر المشتريات", expanded=True):
            with st.form("pur_cat_form"):
                f1, f2 = st.columns(2)
                sel_comp = f1.multiselect("الشركة", df_pur_cat[c_comp].unique() if c_comp else [])
                sel_emp = f2.multiselect("الموظف", df_pur_cat[c_emp].unique() if c_emp else [])
                submit_cat = st.form_submit_button("تطبيق הפلاتر")
        
        df_f = df_pur_cat.copy()
        if sel_comp: df_f = df_f[df_f[c_comp].isin(sel_comp)]
        if sel_emp: df_f = df_f[df_f[c_emp].isin(sel_emp)]

        st.markdown("<br>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("إجمالي المطلوب", f"{df_f[c_req].sum():,.0f}" if c_req else "0")
        k2.metric("إجمالي الرصيد الحالي", f"{df_f[c_cur].sum():,.0f}" if c_cur else "0")
        k3.metric("الشركات الموردة", f"{df_f[c_comp].nunique()}" if c_comp else "0")
        k4.metric("موظفي المتابعة", f"{df_f[c_emp].nunique()}" if c_emp else "0")
        st.markdown("---")

        if c_item and c_req and c_cur:
            top_items = df_f.groupby(c_item)[[c_req, c_cur]].sum().nlargest(10, c_req).reset_index()
            melted = top_items.melt(id_vars=c_item, value_vars=[c_req, c_cur], var_name='النوع', value_name='الكمية')
            fig = px.bar(melted, x=c_item, y='الكمية', color='النوع', barmode='group', title="أعلى 10 مواد: المطلوب مقابل الرصيد", color_discrete_map={c_req: '#f28b82', c_cur: '#8ab4f8'})
            fig.update_layout(**gf_layout, xaxis_title="", legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        custom_analysis_lab(df_f, [c for c in [c_emp, c_comp, c_unit, c_item, c_arr] if c], [c for c in [c_req, c_cur] if c], "pur_cat")
        st.markdown("---")
        with st.expander("قاعدة بيانات المصنفات (Raw Data)"):
            st.dataframe(df_f, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات. اضغط تحديث.")

# ----------------- 7. مشتريات المجزر (القسم الجديد) -----------------
elif st.session_state.active_tab == 'pur_slh':
    df_pur_slh, c_code, c_item, c_cat, c_dept, c_unit, c_cur, c_req, c_comp, c_date, c_status = load_pur_slh_data()
    
    if not df_pur_slh.empty:
        with st.expander("🔍 فلاتر مشتريات المجزر", expanded=True):
            with st.form("pur_slh_form"):
                f1, f2 = st.columns(2)
                sel_comp = f1.multiselect("الشركة", df_pur_slh[c_comp].unique() if c_comp else [])
                sel_stat = f2.multiselect("حالة التوريد", df_pur_slh[c_status].unique() if c_status else [])
                submit_slh = st.form_submit_button("تطبيق הפلاتر")
        
        df_f = df_pur_slh.copy()
        if sel_comp: df_f = df_f[df_f[c_comp].isin(sel_comp)]
        if sel_stat: df_f = df_f[df_f[c_status].isin(sel_stat)]

        st.markdown("<br>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("إجمالي المطلوب سيستم", f"{df_f[c_req].sum():,.0f}" if c_req else "0")
        k2.metric("إجمالي الرصيد الحالي", f"{df_f[c_cur].sum():,.0f}" if c_cur else "0")
        k3.metric("الشركات الموردة", f"{df_f[c_comp].nunique()}" if c_comp else "0")
        k4.metric("المواد المسجلة", f"{df_f[c_item].nunique()}" if c_item else "0")
        st.markdown("---")

        if c_item and c_req and c_comp:
            r1, r2 = st.columns(2)
            with r1:
                st.markdown("### حجم الطلبات حسب الشركة")
                comp_data = df_f.groupby(c_comp)[c_req].sum().reset_index()
                fig_comp = px.pie(comp_data, values=c_req, names=c_comp, hole=0.6, color_discrete_sequence=gf_colors)
                fig_comp.update_layout(**gf_layout)
                st.plotly_chart(fig_comp, use_container_width=True)
            with r2:
                st.markdown("### أعلى 10 مواد مطلوبة")
                top_req = df_f.groupby(c_item)[[c_req, c_cur]].sum().nlargest(10, c_req).reset_index()
                melted = top_req.melt(id_vars=c_item, value_vars=[c_req, c_cur], var_name='النوع', value_name='الكمية')
                fig_bar = px.bar(melted, x=c_item, y='الكمية', color='النوع', barmode='group', color_discrete_map={c_req: '#f28b82', c_cur: '#81c995'})
                fig_bar.update_layout(**gf_layout, xaxis_title="", legend_title_text="")
                st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")
        custom_analysis_lab(df_f, [c for c in [c_comp, c_status, c_cat, c_item] if c], [c for c in [c_req, c_cur] if c], "pur_slh_new")
        st.markdown("---")
        with st.expander("قاعدة بيانات مشتريات المجزر (Raw Data)"):
            st.dataframe(df_f, use_container_width=True)
    else:
        st.warning("⚠️ جاري سحب بيانات مشتريات المجزر، يرجى الانتظار...")
        if st.button("إعادة محاولة الاتصال 🔄"):
            st.cache_data.clear()
            st.rerun()

except Exception as e:
    st.error("🚨 النظام اكتشف خطأ غير متوقع. يرجى مسح الذاكرة أو مراجعة الرابط.")
    st.code(traceback.format_exc())

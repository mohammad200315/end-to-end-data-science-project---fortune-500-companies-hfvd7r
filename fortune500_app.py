import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import warnings
import os
from datetime import datetime
warnings.filterwarnings('ignore')

# إعداد الصفحة
st.set_page_config(
    page_title="Fortune 500 Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# دوال مساعدة للصور والملفات
def get_image_path(filename):
    """البحث عن الصورة في مسارات مختلفة"""
    possible_paths = [
        filename,
        f"images/{filename}",
        f"assets/{filename}",
        filename.replace("2026", "2024"),
        filename.replace("2026", "2025"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# محاولة تحميل صورة الخلفية
image_path = get_image_path("WhatsApp Image 2026-02-11 at 3.32.24 PM.jpeg")
if image_path:
    image_base64 = get_base64_of_image(image_path)
else:
    image_base64 = None

# CSS مخصص للتصميم
if image_base64:
    bg_style = f"""
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    """
else:
    bg_style = """
    .stApp {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
    }
    """

st.markdown(f"""
<style>
{bg_style}

.main > div {{
    background: rgba(0, 0, 0, 0.65) !important;
    backdrop-filter: blur(8px) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    margin: 10px !important;
}}

.css-1d391kg, .css-163ttbj, [data-testid="stSidebar"] > div:first-child {{
    background: rgba(10, 10, 20, 0.85) !important;
    backdrop-filter: blur(10px) !important;
    border-right: 1px solid rgba(255,255,255,0.15) !important;
}}

.custom-card {{
    background: rgba(20, 25, 40, 0.75) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}}

.custom-card h1, .custom-card h2, .custom-card h3, .custom-card h4, 
.custom-card h5, .custom-card h6, .custom-card p, .custom-card span, 
.custom-card div {{
    color: #ffffff !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3) !important;
}}

.stButton > button {{
    background: linear-gradient(135deg, #4A5568 0%, #2D3748 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    transition: all 0.3s ease !important;
}}

.stButton > button:hover {{
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(74, 85, 104, 0.4) !important;
    background: linear-gradient(135deg, #2D3748 0%, #1A202C 100%) !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 12px;
    background: rgba(0,0,0,0.3);
    padding: 8px;
    border-radius: 16px;
    backdrop-filter: blur(5px);
}}

.stTabs [data-baseweb="tab"] {{
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    color: white !important;
    padding: 12px 24px;
    border: 1px solid rgba(255,255,255,0.15);
    font-weight: 500;
    transition: all 0.3s ease;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #4A5568 0%, #2D3748 100%) !important;
    color: white !important;
    border: none;
    box-shadow: 0 4px 12px rgba(74, 85, 104, 0.3);
}}

.stSelectbox, .stDropdown {{
    background: rgba(30, 35, 50, 0.8);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(5px);
}}

.stSelectbox label, .stDropdown label {{
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
}}

.stSelectbox > div > div {{
    background: rgba(40, 45, 60, 0.9) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
}}

h1, h2, h3, h4, h5, h6 {{
    color: #ffffff !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
    letter-spacing: 0.5px !important;
}}

.stMarkdown {{
    color: #ffffff !important;
}}

.stMarkdown p, .stMarkdown span {{
    color: rgba(255,255,255,0.95) !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
}}

.stMetric {{
    background: rgba(30, 35, 50, 0.7) !important;
    backdrop-filter: blur(8px) !important;
    padding: 20px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}}

.stMetric label {{
    color: rgba(255,255,255,0.9) !important;
    font-size: 0.9rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}}

.stMetric div {{
    color: #ffffff !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3) !important;
}}

.dataframe, .stDataFrame {{
    background: rgba(30, 35, 50, 0.8) !important;
    backdrop-filter: blur(8px) !important;
    border-radius: 12px !important;
    padding: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}}

.stDataFrame td, .stDataFrame th {{
    color: #ffffff !important;
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    padding: 12px !important;
}}

.stDataFrame th {{
    background: rgba(74, 85, 104, 0.3) !important;
    color: white !important;
    font-weight: 600 !important;
}}

.stSuccess, .stInfo {{
    background: rgba(30, 35, 50, 0.8) !important;
    backdrop-filter: blur(8px) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px !important;
}}

.stRadio > div {{
    background: rgba(30, 35, 50, 0.6) !important;
    backdrop-filter: blur(8px) !important;
    padding: 15px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}}

.stRadio label {{
    color: white !important;
    font-size: 1rem !important;
    padding: 8px !important;
}}

.stNumberInput > div > div > input {{
    background: rgba(40, 45, 60, 0.9) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
}}

hr {{
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, rgba(160, 174, 192, 0.5), transparent) !important;
    margin: 30px 0 !important;
}}

.sidebar-content p, .sidebar-content span, .sidebar-content div {{
    color: white !important;
}}

div[data-testid="stMetric"]:nth-of-type(1) {{
    background: linear-gradient(135deg, rgba(160, 174, 192, 0.3) 0%, rgba(113, 128, 150, 0.3) 100%) !important;
    border: 1px solid rgba(160, 174, 192, 0.5) !important;
}}

div[data-testid="stMetric"]:nth-of-type(1) label {{
    color: #E2E8F0 !important;
}}

div[data-testid="stMetric"]:nth-of-type(1) div {{
    color: #CBD5E0 !important;
    text-shadow: 1px 1px 3px rgba(160,174,192,0.3) !important;
}}
</style>
""", unsafe_allow_html=True)

# اختيار اللغة
lang = st.sidebar.radio("Language / اللغة", ["English", "العربية"], index=0)

def _(en, ar):
    return en if lang == "English" else ar

# دوال مساعدة
def safe_load_data(file_path, file_description):
    """تحميل آمن مع رسائل خطأ محسنة"""
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def validate_year_column(df):
    """التحقق من عمود السنة وإصلاحه إذا لزم الأمر"""
    current_year = datetime.now().year
    if 'year' in df.columns:
        # تصحيح السنوات المستقبلية
        df['year'] = df['year'].apply(lambda x: current_year if x > current_year + 1 else x)
    return df

def add_export_button(dataframe, filename, key):
    """إضافة زر تصدير البيانات"""
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'''
    <a href="data:file/csv;base64,{b64}" 
       download="{filename}.csv" 
       style="background: #4A5568; 
              color: white; 
              padding: 8px 16px; 
              border-radius: 8px; 
              text-decoration: none; 
              margin: 5px 0; 
              display: inline-block;
              font-size: 0.9rem;
              border: 1px solid rgba(255,255,255,0.2);
              transition: all 0.3s ease;"
       onmouseover="this.style.background='#2D3748'"
       onmouseout="this.style.background='#4A5568'">
        📥 {_("Export CSV", "تصدير CSV")}
    </a>
    '''
    return href

# تحميل البيانات
@st.cache_data
def load_data():
    files = {}
    
    # تحميل الملفات المحلية
    files['main'] = safe_load_data('fortune500_cleaned.csv', "Main Data")
    files['pred2024'] = safe_load_data('fortune500_2024_predictions.csv', "2024 Predictions")
    files['models'] = safe_load_data('fortune500_models_performance.csv', "Models Performance")
    files['test'] = safe_load_data('fortune500_test_predictions.csv', "Test Predictions")
    
    return files

# الشريط الجانبي
with st.sidebar:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(45, 55, 72, 0.25) 0%, rgba(26, 32, 44, 0.25) 100%);
                backdrop-filter: blur(12px);
                padding: 25px; 
                border-radius: 20px; 
                margin-bottom: 25px;
                border: 1px solid rgba(255,255,255,0.2);">
        <h3 style="color: white; margin-top: 0; font-size: 1.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
            {_('Control Panel', 'لوحة التحكم')}
        </h3>
        <p style="color: rgba(255,255,255,0.9); margin-bottom: 0; font-size: 1rem;">
            {_('Developer: Mohammad Naser', 'المطور: محمد زكريا ناصر')}
        </p>
        <p style="color: rgba(255,255,255,0.7); margin-bottom: 0; font-size: 0.9rem;">
            {_('Data Analyst', 'محلل بيانات')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # قسم رفع الملفات
    with st.expander(_("📁 Upload Files", "📁 رفع الملفات")):
        st.caption(_("Upload missing CSV files", "رفع ملفات CSV المفقودة"))
        uploaded_main = st.file_uploader(_("Main Data", "البيانات الرئيسية"), type=['csv'], key='main_upload')
        uploaded_pred = st.file_uploader(_("2024 Predictions", "توقعات 2024"), type=['csv'], key='pred_upload')
    
    # إعدادات متقدمة
    with st.expander(_("⚙️ Advanced Settings", "⚙️ إعدادات متقدمة")):
        show_animations = st.checkbox(_("Show Animations", "عرض الحركات"), True)
        default_companies = st.slider(_("Default Companies Count", "عدد الشركات الافتراضي"), 5, 30, 15)
        chart_theme = st.selectbox(_("Chart Theme", "ثيم الرسوم"), 
                                  [_("Dark", "داكن"), _("Light", "فاتح")], 
                                  index=0)
    
    # قائمة التحليل
    st.markdown("---")
    menu = st.radio(
        _("Select Analysis", "اختر التحليل"),
        [
            _("📊 Dashboard", "📊 لوحة المعلومات"),
            _("📅 Year Analysis", "📅 تحليل السنوات"),
            _("🏢 Company Analysis", "🏢 تحليل الشركات"),
            _("🔄 Company Comparison", "🔄 مقارنة الشركات"),
            _("📈 Year Comparison", "📈 مقارنة السنوات"),
            _("🤖 Predictions & Models", "🤖 التوقعات والنماذج"),
            _("📋 Data Overview", "📋 نظرة عامة")
        ]
    )

# تحميل البيانات
with st.spinner(_("Loading data...", "جاري تحميل البيانات...")):
    data = load_data()
    
    # استخدام الملفات المرفوعة إذا وجدت
    if 'uploaded_main' in locals() and uploaded_main is not None:
        data['main'] = pd.read_csv(uploaded_main)
    if 'uploaded_pred' in locals() and uploaded_pred is not None:
        data['pred2024'] = pd.read_csv(uploaded_pred)

df = data['main']

if df.empty:
    st.error(_("Main data file not found! Please upload the file.", 
               "ملف البيانات الرئيسي غير موجود! الرجاء رفع الملف."))
    st.stop()

# معالجة البيانات
df = validate_year_column(df)
df['profit_margin'] = (df['profit_mil'] / df['revenue_mil']) * 100
df['revenue_bil'] = df['revenue_mil'] / 1000
df['profit_bil'] = df['profit_mil'] / 1000

# ألوان مخصصة
colors = {
    'primary': '#4A5568',
    'secondary': '#2D3748',
    'accent1': '#A0AEC0',
    'accent2': '#718096',
    'success': '#48BB78',
    'danger': '#F56565',
    'warning': '#ECC94B',
    'info': '#A0AEC0'
}

# الهيدر الرئيسي
st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(45, 55, 72, 0.95) 0%, rgba(26, 32, 44, 0.95) 100%);
            backdrop-filter: blur(12px);
            padding: 40px; 
            border-radius: 25px; 
            margin-bottom: 30px; 
            text-align: center;
            border: 1px solid rgba(255,255,255,0.25);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
    <h1 style="color: white; margin: 0; font-size: 3.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-weight: 700; letter-spacing: 1px;">
        {_('Fortune 500 Analytics Dashboard', 'لوحة تحليل Fortune 500')}
    </h1>
    <p style="color: rgba(255,255,255,0.95); margin-top: 15px; font-size: 1.4rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
        {_('1996-2024 Analysis & Predictions', 'تحليل وتوقعات 1996-2024')}
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if menu == _("📊 Dashboard", "📊 لوحة المعلومات"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("📊 Executive Dashboard", "📊 لوحة المعلومات التنفيذية"))
    
    # مؤشرات سريعة
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        latest_year = df['year'].max()
        st.metric(_("📅 Latest Year", "📅 آخر سنة"), latest_year)
    with col2:
        total_revenue_latest = df[df['year'] == latest_year]['revenue_bil'].sum()
        st.metric(_("💰 Total Revenue", "💰 إجمالي الإيرادات"), f"${total_revenue_latest:,.1f}B")
    with col3:
        avg_margin = df[df['year'] == latest_year]['profit_margin'].mean()
        st.metric(_("📊 Avg Margin", "📊 متوسط الهامش"), f"{avg_margin:.1f}%")
    with col4:
        top_company = df[df['year'] == latest_year].nlargest(1, 'revenue_mil')['name'].iloc[0]
        st.metric(_("🏆 Top Company", "🏆 أفضل شركة"), top_company)
    
    # رسوم بيانية سريعة
    col1, col2 = st.columns(2)
    with col1:
        # توزيع الصناعات
        industry_counts = df[df['year'] == latest_year]['industry'].value_counts().head(10)
        fig_ind = px.pie(values=industry_counts.values, names=industry_counts.index,
                        title=_(f"Top Industries {latest_year}", f"أهم الصناعات {latest_year}"),
                        color_discrete_sequence=[colors['accent1'], colors['accent2'], 
                                                colors['success'], colors['warning']])
        fig_ind.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'), height=400)
        st.plotly_chart(fig_ind, use_container_width=True)
    
    with col2:
        # أفضل 10 شركات
        top_10 = df[df['year'] == latest_year].nlargest(10, 'revenue_bil')
        fig_top = px.bar(top_10, x='revenue_bil', y='name', orientation='h',
                        title=_("Top 10 Companies by Revenue", "أفضل 10 شركات بالإيرادات"),
                        color='revenue_bil', color_continuous_scale='gray')
        fig_top.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            height=400, font=dict(color='white'))
        st.plotly_chart(fig_top, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== YEAR ANALYSIS ====================
elif menu == _("📅 Year Analysis", "📅 تحليل السنوات"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("📅 Year Analysis", "📅 تحليل السنوات"))
    
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        year = st.selectbox(_("Select Year", "اختر السنة"), sorted(df['year'].unique(), reverse=True))
    with col2:
        top_n = st.number_input(_("Companies", "الشركات"), 5, 50, default_companies)
    with col3:
        st.markdown(add_export_button(df[df['year'] == year], f"fortune500_{year}_data", "year_export"), 
                   unsafe_allow_html=True)
    
    df_year = df[df['year'] == year]
    
    if not df_year.empty:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(_("Companies", "الشركات"), f"{len(df_year):,}")
        with col2:
            st.metric(_("Total Revenue", "إجمالي الإيرادات"), f"${df_year['revenue_bil'].sum():,.1f}B")
        with col3:
            st.metric(_("Avg Revenue", "متوسط الإيرادات"), f"${df_year['revenue_bil'].mean():,.1f}B")
        with col4:
            st.metric(_("Avg Margin", "متوسط الهامش"), f"{df_year['profit_margin'].mean():.1f}%")
        
        # Tabs
        tabs = st.tabs([
            _("🏆 Top Companies", "🏆 أفضل الشركات"), 
            _("📊 Revenue Distribution", "📊 توزيع الإيرادات"), 
            _("🏭 Industry Analysis", "🏭 تحليل الصناعات"),
            _("📈 Growth Analysis", "📈 تحليل النمو"),
            _("📊 Statistics", "📊 إحصائيات متقدمة")
        ])
        
        with tabs[0]:
            top = df_year.nlargest(top_n, 'revenue_mil')
            fig = px.bar(top, x='revenue_bil', y='name', orientation='h',
                        title=f"{_('Top', 'أفضل')} {top_n} {_('Companies', 'شركة')} - {year}",
                        color='revenue_bil', color_continuous_scale='gray')
            fig.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                            font=dict(color='white', size=12), title_font_color='white')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(top[['rank','name','revenue_bil','profit_bil','profit_margin','industry']], 
                        use_container_width=True)
        
        with tabs[1]:
            fig = px.histogram(df_year, x='revenue_bil', nbins=50, 
                              title=_("Revenue Distribution (Billions $)", "توزيع الإيرادات (بالمليارات)"))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                            height=400, font=dict(color='white'), title_font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        with tabs[2]:
            ind = df_year.groupby('industry').agg({
                'revenue_bil': 'sum',
                'profit_bil': 'sum',
                'profit_margin': 'mean'
            }).sort_values('revenue_bil', ascending=False).head(15)
            
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(ind.reset_index(), x='revenue_bil', y='industry', orientation='h',
                            title=_("Revenue by Industry (B$)", "الإيرادات حسب الصناعة"),
                            color='revenue_bil', color_continuous_scale='gray')
                fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                 height=500, font=dict(color='white'), title_font_color='white')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.bar(ind.reset_index(), x='profit_margin', y='industry', orientation='h',
                            title=_("Margin by Industry", "الهامش حسب الصناعة"),
                            color='profit_margin', color_continuous_scale='gray')
                fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                 height=500, font=dict(color='white'), title_font_color='white')
                st.plotly_chart(fig2, use_container_width=True)
        
        with tabs[3]:
            # حساب معدلات النمو
            prev_year = df[df['year'] == year - 1]
            if not prev_year.empty:
                growth_df = pd.merge(
                    df_year[['name', 'revenue_bil']],
                    prev_year[['name', 'revenue_bil']],
                    on='name',
                    suffixes=('_current', '_prev'),
                    how='inner'
                )
                growth_df['growth'] = ((growth_df['revenue_bil_current'] - growth_df['revenue_bil_prev']) / 
                                       growth_df['revenue_bil_prev'] * 100)
                top_growth = growth_df.nlargest(10, 'growth')
                
                if not top_growth.empty:
                    fig_growth = px.bar(top_growth, x='growth', y='name',
                                       title=_("Top 10 Growth Companies", "أسرع 10 شركات نمواً"),
                                       color='growth', color_continuous_scale='greens')
                    fig_growth.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                           height=400, font=dict(color='white'))
                    st.plotly_chart(fig_growth, use_container_width=True)
                else:
                    st.info(_("No growth data available", "لا توجد بيانات نمو متاحة"))
            else:
                st.info(_("Previous year data not available", "بيانات السنة السابقة غير متاحة"))
        
        with tabs[4]:
            st.subheader(_("Statistical Summary", "ملخص إحصائي"))
            stats = df_year[['revenue_bil', 'profit_bil', 'profit_margin']].describe()
            st.dataframe(stats, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== COMPANY ANALYSIS ====================
elif menu == _("🏢 Company Analysis", "🏢 تحليل الشركات"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("🏢 Company Analysis", "🏢 تحليل الشركات"))
    
    company = st.selectbox(_("Select Company", "اختر الشركة"), sorted(df['name'].unique()))
    df_comp = df[df['name'] == company].sort_values('year')
    
    if not df_comp.empty:
        latest = df_comp.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(_("Years in List", "السنوات في القائمة"), len(df_comp))
        with col2:
            st.metric(_("Latest Revenue", "آخر إيرادات"), f"${latest['revenue_bil']:,.1f}B")
        with col3:
            st.metric(_("Latest Rank", "آخر ترتيب"), f"#{int(latest['rank'])}")
        with col4:
            st.metric(_("Latest Margin", "آخر هامش"), f"{latest['profit_margin']:.1f}%")
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(df_comp, x='year', y='revenue_bil', 
                          title=_("Revenue Trend (Billions $)", "اتجاه الإيرادات (بالمليارات)"), 
                          markers=True)
            fig1.update_traces(line=dict(color=colors['accent1'], width=3), 
                              marker=dict(color=colors['accent1'], size=8))
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                             height=400, font=dict(color='white'), title_font_color='white')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.line(df_comp, x='year', y='rank', 
                          title=_("Rank Trend", "اتجاه الترتيب"), 
                          markers=True)
            fig2.update_traces(line=dict(color=colors['accent2'], width=3), 
                              marker=dict(color=colors['accent2'], size=8))
            fig2.update_yaxes(autorange="reversed")
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                             height=400, font=dict(color='white'), title_font_color='white')
            st.plotly_chart(fig2, use_container_width=True)
        
        st.subheader(_("Historical Data", "البيانات التاريخية"))
        st.dataframe(df_comp[['year','rank','revenue_bil','profit_bil','profit_margin']], 
                    use_container_width=True)
        
        # زر التصدير
        st.markdown(add_export_button(df_comp, f"{company}_history", "company_export"), 
                   unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== COMPANY COMPARISON ====================
elif menu == _("🔄 Company Comparison", "🔄 مقارنة الشركات"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("🔄 Multi-Company Comparison", "🔄 مقارنة متعددة الشركات"))
    
    companies = st.multiselect(
        _("Select Companies (2-5)", "اختر الشركات (2-5)"),
        sorted(df['name'].unique()),
        default=sorted(df['name'].unique())[:3]
    )
    
    if len(companies) >= 2:
        df_compare = df[df['name'].isin(companies)]
        
        # مقارنة الإيرادات
        fig1 = px.line(df_compare, x='year', y='revenue_bil', color='name',
                      title=_("Revenue Comparison (Billions $)", "مقارنة الإيرادات (بالمليارات)"),
                      color_discrete_sequence=[colors['accent1'], colors['success'], 
                                              colors['warning'], colors['danger']])
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         height=400, font=dict(color='white'), title_font_color='white')
        st.plotly_chart(fig1, use_container_width=True)
        
        # مقارنة الهامش
        fig2 = px.line(df_compare, x='year', y='profit_margin', color='name',
                      title=_("Profit Margin Comparison", "مقارنة هامش الربح"),
                      color_discrete_sequence=[colors['accent1'], colors['success'], 
                                              colors['warning'], colors['danger']])
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         height=400, font=dict(color='white'), title_font_color='white')
        st.plotly_chart(fig2, use_container_width=True)
        
        # جدول المقارنة
        latest_year = df['year'].max()
        comparison_table = df_compare[df_compare['year'] == latest_year][
            ['name', 'rank', 'revenue_bil', 'profit_bil', 'profit_margin']
        ].sort_values('revenue_bil', ascending=False)
        
        st.subheader(_(f"Latest Data ({latest_year})", f"أحدث البيانات ({latest_year})"))
        st.dataframe(comparison_table, use_container_width=True)
    
    else:
        st.warning(_("Please select at least 2 companies", "الرجاء اختيار شركتين على الأقل"))
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== YEAR COMPARISON ====================
elif menu == _("📈 Year Comparison", "📈 مقارنة السنوات"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("📈 Year Comparison", "📈 مقارنة السنوات"))
    
    years = sorted(df['year'].unique(), reverse=True)
    col1, col2 = st.columns(2)
    with col1:
        y1 = st.selectbox(_("First Year", "السنة الأولى"), years, index=3)
    with col2:
        y2 = st.selectbox(_("Second Year", "السنة الثانية"), years, index=0)
    
    if y1 != y2:
        d1 = df[df['year'] == y1]
        d2 = df[df['year'] == y2]
        
        rev_growth = ((d2['revenue_bil'].sum() - d1['revenue_bil'].sum()) / d1['revenue_bil'].sum()) * 100
        avg_growth = ((d2['revenue_bil'].mean() - d1['revenue_bil'].mean()) / d1['revenue_bil'].mean()) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(_("Revenue Growth", "نمو الإيرادات"), f"{rev_growth:+.1f}%")
        with col2:
            st.metric(_("Avg Growth", "متوسط النمو"), f"{avg_growth:+.1f}%")
        with col3:
            st.metric(_("Companies Change", "تغير الشركات"), f"{len(d2)-len(d1):+d}")
        
        comp = pd.DataFrame({
            _("Year", "السنة"): [str(y1), str(y2)],
            _("Total Revenue (B$)", "إجمالي الإيرادات"): [d1['revenue_bil'].sum(), d2['revenue_bil'].sum()],
            _("Avg Revenue (B$)", "متوسط الإيرادات"): [d1['revenue_bil'].mean(), d2['revenue_bil'].mean()],
            _("Companies", "الشركات"): [len(d1), len(d2)]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name=_("Total Revenue", "إجمالي الإيرادات"), 
                            x=comp[_("Year", "السنة")], y=comp[_("Total Revenue (B$)", "إجمالي الإيرادات")],
                            marker_color=colors['accent1']))
        fig.add_trace(go.Bar(name=_("Avg Revenue", "متوسط الإيرادات"), 
                            x=comp[_("Year", "السنة")], y=comp[_("Avg Revenue (B$)", "متوسط الإيرادات")],
                            marker_color=colors['accent2']))
        fig.update_layout(barmode='group', height=400, 
                         plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                         font=dict(color='white', size=12), title_font_color='white',
                         legend_font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(add_export_button(comp, f"comparison_{y1}_{y2}", "compare_export"), 
                   unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREDICTIONS & MODELS ====================
elif menu == _("🤖 Predictions & Models", "🤖 التوقعات والنماذج"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("🤖 Predictions & AI Models", "🤖 التوقعات والنماذج الذكية"))
    
    if not data['pred2024'].empty:
        st.subheader(_("📊 2024 Predictions", "📊 توقعات 2024"))
        df_pred = data['pred2024']
        
        # محاولة تحديد الأعمدة تلقائياً
        revenue_col = None
        name_col = None
        rank_col = None
        
        for col in df_pred.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['revenue', 'rev', 'pred', 'forecast']):
                revenue_col = col
            if any(x in col_lower for x in ['name', 'company', 'corporation']):
                name_col = col
            if 'rank' in col_lower:
                rank_col = col
        
        if revenue_col is None and len(df_pred.select_dtypes(include=[np.number]).columns) > 0:
            revenue_col = df_pred.select_dtypes(include=[np.number]).columns[0]
        
        display_cols = []
        if name_col:
            display_cols.append(name_col)
        if revenue_col:
            # تحويل إلى مليارات إذا كانت الأرقام كبيرة
            df_pred['revenue_bil_pred'] = df_pred[revenue_col] / 1000
            display_cols.append('revenue_bil_pred')
        if rank_col:
            display_cols.append(rank_col)
        
        if revenue_col and name_col:
            df_pred_sorted = df_pred.sort_values(revenue_col, ascending=False).head(20)
            fig = px.bar(df_pred_sorted, x=revenue_col, y=name_col, orientation='h',
                        title=_("Top 20 Predicted Companies 2024", "أفضل 20 شركة متوقعة 2024"),
                        color=revenue_col, color_continuous_scale='gray')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                            height=500, font=dict(color='white'), title_font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        
        if display_cols:
            st.dataframe(df_pred[display_cols].head(50), use_container_width=True)
            st.markdown(add_export_button(df_pred[display_cols], "predictions_2024", "pred_export"), 
                       unsafe_allow_html=True)
        else:
            st.dataframe(df_pred.head(50), use_container_width=True)
    else:
        st.info(_("📁 2024 predictions file not available. Please upload the file.",
                 "📁 ملف توقعات 2024 غير متوفر. الرجاء رفع الملف."))
    
    if not data['models'].empty:
        st.subheader(_("📈 Model Performance", "📈 أداء النماذج"))
        df_models = data['models']
        
        model_col = None
        accuracy_col = None
        
        for col in df_models.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['model', 'name', 'algorithm']):
                model_col = col
            if any(x in col_lower for x in ['acc', 'score', 'r2', 'mae', 'mse']):
                accuracy_col = col
        
        if accuracy_col:
            if model_col:
                fig = px.bar(df_models, x=model_col, y=accuracy_col, 
                           title=_("Model Performance Comparison", "مقارنة أداء النماذج"),
                           color=accuracy_col, color_continuous_scale='gray')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                height=400, xaxis_tickangle=45, font=dict(color='white'), 
                                title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.bar(df_models, y=accuracy_col, 
                           title=_("Model Performance", "أداء النماذج"),
                           color=accuracy_col, color_continuous_scale='gray')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                height=400, font=dict(color='white'), title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df_models, use_container_width=True)
    
    if not data['test'].empty:
        st.subheader(_("🧪 Test Predictions", "🧪 توقعات الاختبار"))
        df_test = data['test']
        
        actual_col = None
        predicted_col = None
        
        for col in df_test.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['actual', 'true', 'real']):
                actual_col = col
            if any(x in col_lower for x in ['pred', 'predict', 'forecast']):
                predicted_col = col
        
        if actual_col and predicted_col:
            fig = px.scatter(df_test.head(100), x=actual_col, y=predicted_col,
                           title=_("Actual vs Predicted", "الفعلية مقابل المتوقعة"),
                           labels={actual_col: _("Actual", "فعلية"), 
                                  predicted_col: _("Predicted", "متوقعة")})
            fig.update_traces(marker=dict(color=colors['accent1'], size=5))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                            height=500, font=dict(color='white'), title_font_color='white')
            
            # إضافة خط y=x للمقارنة
            max_val = max(df_test[actual_col].max(), df_test[predicted_col].max())
            fig.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val],
                                    mode='lines', name='Perfect Prediction',
                                    line=dict(color='white', dash='dash')))
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df_test.head(50), use_container_width=True)
        st.markdown(add_export_button(df_test.head(100), "test_predictions", "test_export"), 
                   unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== DATA OVERVIEW ====================
else:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("📋 Data Overview", "📋 نظرة عامة"))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(_("Total Years", "إجمالي السنوات"), df['year'].nunique())
    with col2:
        st.metric(_("Unique Companies", "الشركات الفريدة"), df['name'].nunique())
    with col3:
        st.metric(_("Total Revenue", "إجمالي الإيرادات"), f"${df['revenue_bil'].sum()/1000:,.1f}T")
    with col4:
        avg_growth = df.groupby('year')['revenue_bil'].mean().pct_change().mean() * 100
        st.metric(_("Avg Annual Growth", "متوسط النمو السنوي"), f"{avg_growth:.1f}%")
    
    # اتجاهات متعددة
    yearly = df.groupby('year').agg({
        'revenue_bil': 'mean',
        'profit_bil': 'mean',
        'profit_margin': 'mean',
        'revenue_bil': 'sum'
    }).reset_index()
    yearly.columns = ['year', 'avg_revenue', 'avg_profit', 'avg_margin', 'total_revenue']
    
    fig = make_subplots(rows=3, cols=1, 
                       subplot_titles=(
                           _("Total Revenue Trend (B$)", "اتجاه إجمالي الإيرادات"),
                           _("Average Profit Trend (B$)", "اتجاه متوسط الأرباح"),
                           _("Average Margin Trend", "اتجاه متوسط الهامش")
                       ))
    
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['total_revenue'], 
                            name=_("Total Revenue","إجمالي الإيرادات"), 
                            line=dict(color=colors['accent1'], width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['avg_profit'], 
                            name=_("Avg Profit","متوسط الأرباح"), 
                            line=dict(color=colors['success'], width=3)), row=2, col=1)
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['avg_margin'], 
                            name=_("Avg Margin","متوسط الهامش"), 
                            line=dict(color=colors['warning'], width=3)), row=3, col=1)
    
    fig.update_layout(height=700, showlegend=True, 
                     plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                     font=dict(color='white', size=12), title_font_color='white',
                     legend_font_color='white')
    
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)', gridwidth=1)
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)', gridwidth=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # أفضل الشركات عبر التاريخ
    st.subheader(_("🏆 Top Companies All Time", "🏆 أفضل الشركات على الإطلاق"))
    top = df.groupby('name')['revenue_bil'].max().nlargest(15)
    fig2 = px.bar(x=top.values, y=top.index, orientation='h',
                 title=_("Top 15 Companies by Max Revenue", "أفضل 15 شركة بأقصى إيرادات"),
                 color=top.values, color_continuous_scale='gray')
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                      height=500, font=dict(color='white', size=12), title_font_color='white')
    st.plotly_chart(fig2, use_container_width=True)
    
    # إحصائيات عامة
    st.subheader(_("📊 General Statistics", "📊 إحصائيات عامة"))
    stats = df[['revenue_bil', 'profit_bil', 'profit_margin']].describe()
    st.dataframe(stats, use_container_width=True)
    
    st.markdown(add_export_button(df.head(1000), "fortune500_full_data", "overview_export"), 
               unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# الفوتر
st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(45, 55, 72, 0.9) 0%, rgba(26, 32, 44, 0.9) 100%);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 30px;
            margin-top: 40px;
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;">
    <p style="color: white; font-size: 1.3rem; margin-bottom: 15px; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
        <strong>{_('Fortune 500 Analytics Dashboard', 'لوحة تحليل Fortune 500')}</strong>
    </p>
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 15px; flex-wrap: wrap;">
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">
            {_('Developed by: Mohammad Naser', 'تم التطوير بواسطة: محمد زكريا ناصر')}
        </p>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">
            {_('Data Analyst', 'محلل بيانات')}
        </p>
    </div>
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 15px; flex-wrap: wrap;">
        <p style="color: rgba(255,255,255,0.8); font-size: 0.95rem;">
            1996-{datetime.now().year}
        </p>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.95rem;">
            {_('Powered by Streamlit & Plotly', 'بتقنية Streamlit و Plotly')}
        </p>
    </div>
    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 10px;">
        © {datetime.now().year} {_('All Rights Reserved', 'جميع الحقوق محفوظة')}
    </p>
</div>
""", unsafe_allow_html=True)

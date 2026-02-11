import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Fortune 500 Analytics Dashboard",
    page_icon="WhatsApp Image 2026-02-11 at 3.17.53 PM.jpeg",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.custom-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid #e0e0e0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
.custom-card h1, .custom-card h2, .custom-card h3, .custom-card h4, .custom-card h5, .custom-card h6,
.custom-card p, .custom-card span, .custom-card div {
    color: #000000 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #5E3A8A 0%, #3B82F6 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
    color: white;
    padding: 10px 20px;
    border: 1px solid rgba(255,255,255,0.2);
}
.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.25);
    color: white;
}
.stSelectbox, .stDropdown {
    background: white;
    border-radius: 8px;
}
.stSelectbox label, .stDropdown label {
    color: white !important;
}
h1, h2, h3, h4, h5, h6 {
    color: white !important;
}
.stMarkdown {
    color: white !important;
}
.stMetric {
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.stMetric label, .stMetric div {
    color: #000000 !important;
}
.dataframe {
    color: #000000 !important;
}
.stDataFrame {
    color: #000000 !important;
}
.stDataFrame td, .stDataFrame th {
    color: #000000 !important;
}
.footer {
    text-align: center;
    color: rgba(255,255,255,0.7);
    padding: 20px;
    font-size: 14px;
}
.developer {
    background: rgba(255,255,255,0.15);
    padding: 15px;
    border-radius: 10px;
    margin-top: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

lang = st.sidebar.radio("Language / اللغة", ["English", "العربية"], index=0)

def _(en, ar):
    return en if lang == "English" else ar

@st.cache_data
def load_data():
    files = {}
    try:
        files['main'] = pd.read_csv('fortune500_cleaned.csv')
        st.sidebar.success(f"Main: {len(files['main']):,} rows")
    except:
        files['main'] = pd.DataFrame()
    try:
        files['pred2024'] = pd.read_csv('fortune500_2024_predictions.csv')
        st.sidebar.success(f"2024: {len(files['pred2024']):,} rows")
    except:
        files['pred2024'] = pd.DataFrame()
    try:
        files['models'] = pd.read_csv('fortune500_models_performance.csv')
        st.sidebar.success(f"Models: {len(files['models'])} models")
    except:
        files['models'] = pd.DataFrame()
    try:
        files['test'] = pd.read_csv('fortune500_test_predictions.csv')
        st.sidebar.success(f"Test: {len(files['test']):,} rows")
    except:
        files['test'] = pd.DataFrame()
    return files

data = load_data()
df = data['main']

if df.empty:
    st.error(_("Main data file not found!", "ملف البيانات الرئيسي غير موجود!"))
    st.stop()

df['profit_margin'] = (df['profit_mil'] / df['revenue_mil']) * 100

colors = {
    'primary': '#5E3A8A',
    'secondary': '#3B82F6',
    'accent1': '#10B981',
    'accent2': '#8B5CF6',
    'accent3': '#F59E0B',
    'success': '#10B981',
    'danger': '#EF4444'
}

st.markdown(f"""
<div style="background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center;">
    <h1 style="color: white; margin: 0; font-size: 2.8rem;">{_('Fortune 500 Analytics Dashboard', 'لوحة تحليل Fortune 500')}</h1>
    <p style="color: rgba(255,255,255,0.9); margin-top: 10px; font-size: 1.2rem;">
        {_('1996-2024 Analysis & Predictions', 'تحليل وتوقعات 1996-2024')}
    </p>
    <div style="background: rgba(255,255,255,0.15); padding: 10px; border-radius: 10px; margin-top: 20px; border: 1px solid rgba(255,255,255,0.2);">
        <p style="color: white; margin: 0; font-size: 1.1rem;">
            {_('Developed by: Mohammad Naser', 'تم التطوير بواسطة: محمد زكريا ناصر')}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <h3 style="color: white; margin-top: 0;">{_('Control Panel', 'لوحة التحكم')}</h3>
        <p style="color: rgba(255,255,255,0.8); margin-bottom: 0; font-size: 0.9rem;">
            {_('Developer: Mohammad Naser', 'المطور: محمد زكريا ناصر')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    menu = st.radio(
        _("Select Analysis", "اختر التحليل"),
        [
            _("Year Analysis", "تحليل السنوات"),
            _("Company Analysis", "تحليل الشركات"),
            _("Year Comparison", "مقارنة السنوات"),
            _("Predictions & Models", "التوقعات والنماذج"),
            _("Data Overview", "نظرة عامة")
        ]
    )

if menu == _("Year Analysis", "تحليل السنوات"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("Year Analysis", "تحليل السنوات"))
    col1, col2 = st.columns([3,1])
    with col1:
        year = st.selectbox(_("Select Year", "اختر السنة"), sorted(df['year'].unique(), reverse=True))
    with col2:
        top_n = st.number_input(_("Companies", "الشركات"), 5, 50, 15)
    df_year = df[df['year'] == year]
    if not df_year.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(_("Companies", "الشركات"), f"{len(df_year):,}")
        with col2:
            st.metric(_("Total Revenue", "إجمالي الإيرادات"), f"${df_year['revenue_mil'].sum():,.0f}M")
        with col3:
            st.metric(_("Avg Revenue", "متوسط الإيرادات"), f"${df_year['revenue_mil'].mean():,.0f}M")
        with col4:
            st.metric(_("Avg Margin", "متوسط الهامش"), f"{df_year['profit_margin'].mean():.1f}%")
        tabs = st.tabs([_("Top Companies", "أفضل الشركات"), _("Revenue Distribution", "توزيع الإيرادات"), _("Industry Analysis", "تحليل الصناعات")])
        with tabs[0]:
            top = df_year.nlargest(top_n, 'revenue_mil')
            fig = px.bar(top, x='revenue_mil', y='name', orientation='h',
                        title=f"{_('Top', 'أفضل')} {top_n} {_('Companies', 'شركة')} - {year}",
                        color='revenue_mil', color_continuous_scale='viridis')
            fig.update_layout(height=500, plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#000000'))
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(top[['rank','name','revenue_mil','profit_mil','profit_margin','industry']], use_container_width=True)
        with tabs[1]:
            fig = px.histogram(df_year, x='revenue_mil', nbins=50, title=_("Revenue Distribution", "توزيع الإيرادات"))
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=400, font=dict(color='#000000'))
            st.plotly_chart(fig, use_container_width=True)
        with tabs[2]:
            ind = df_year.groupby('industry').agg({'revenue_mil':'sum','profit_margin':'mean'}).sort_values('revenue_mil', ascending=False).head(15)
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(ind.reset_index(), x='revenue_mil', y='industry', orientation='h',
                            title=_("Revenue by Industry", "الإيرادات حسب الصناعة"))
                fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=500, font=dict(color='#000000'))
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = px.bar(ind.reset_index(), x='profit_margin', y='industry', orientation='h',
                            title=_("Margin by Industry", "الهامش حسب الصناعة"))
                fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=500, font=dict(color='#000000'))
                st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == _("Company Analysis", "تحليل الشركات"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("Company Analysis", "تحليل الشركات"))
    company = st.selectbox(_("Select Company", "اختر الشركة"), sorted(df['name'].unique()))
    df_comp = df[df['name'] == company].sort_values('year')
    if not df_comp.empty:
        latest = df_comp.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(_("Years in List", "السنوات في القائمة"), len(df_comp))
        with col2:
            st.metric(_("Latest Revenue", "آخر إيرادات"), f"${latest['revenue_mil']:,.0f}M")
        with col3:
            st.metric(_("Latest Rank", "آخر ترتيب"), f"#{int(latest['rank'])}")
        with col4:
            st.metric(_("Latest Margin", "آخر هامش"), f"{latest['profit_margin']:.1f}%")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(df_comp, x='year', y='revenue_mil', title=_("Revenue Trend", "اتجاه الإيرادات"), markers=True)
            fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=400, font=dict(color='#000000'))
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.line(df_comp, x='year', y='rank', title=_("Rank Trend", "اتجاه الترتيب"), markers=True)
            fig2.update_yaxes(autorange="reversed")
            fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=400, font=dict(color='#000000'))
            st.plotly_chart(fig2, use_container_width=True)
        st.subheader(_("Historical Data", "البيانات التاريخية"))
        st.dataframe(df_comp[['year','rank','revenue_mil','profit_mil','profit_margin']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == _("Year Comparison", "مقارنة السنوات"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("Year Comparison", "مقارنة السنوات"))
    years = sorted(df['year'].unique(), reverse=True)
    col1, col2 = st.columns(2)
    with col1:
        y1 = st.selectbox(_("First Year", "السنة الأولى"), years, index=3)
    with col2:
        y2 = st.selectbox(_("Second Year", "السنة الثانية"), years, index=0)
    if y1 != y2:
        d1 = df[df['year'] == y1]
        d2 = df[df['year'] == y2]
        rev_growth = ((d2['revenue_mil'].sum() - d1['revenue_mil'].sum()) / d1['revenue_mil'].sum()) * 100
        avg_growth = ((d2['revenue_mil'].mean() - d1['revenue_mil'].mean()) / d1['revenue_mil'].mean()) * 100
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(_("Revenue Growth", "نمو الإيرادات"), f"{rev_growth:+.1f}%")
        with col2:
            st.metric(_("Avg Growth", "متوسط النمو"), f"{avg_growth:+.1f}%")
        with col3:
            st.metric(_("Companies Change", "تغير الشركات"), f"{len(d2)-len(d1):+d}")
        comp = pd.DataFrame({
            _("Year", "السنة"): [str(y1), str(y2)],
            _("Total Revenue", "إجمالي الإيرادات"): [d1['revenue_mil'].sum(), d2['revenue_mil'].sum()],
            _("Avg Revenue", "متوسط الإيرادات"): [d1['revenue_mil'].mean(), d2['revenue_mil'].mean()],
            _("Companies", "الشركات"): [len(d1), len(d2)]
        })
        fig = go.Figure()
        fig.add_trace(go.Bar(name=_("Total Revenue", "إجمالي الإيرادات"), x=comp[_("Year", "السنة")], y=comp[_("Total Revenue", "إجمالي الإيرادات")]))
        fig.add_trace(go.Bar(name=_("Avg Revenue", "متوسط الإيرادات"), x=comp[_("Year", "السنة")], y=comp[_("Avg Revenue", "متوسط الإيرادات")]))
        fig.update_layout(barmode='group', height=400, plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#000000'))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == _("Predictions & Models", "التوقعات والنماذج"):
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("Predictions & AI Models", "التوقعات والنماذج الذكية"))
    
    if not data['pred2024'].empty:
        st.subheader(_("2024 Predictions", "توقعات 2024"))
        df_pred = data['pred2024']
        
        revenue_col = None
        name_col = None
        rank_col = None
        
        for col in df_pred.columns:
            col_lower = col.lower()
            if 'revenue' in col_lower or 'rev' in col_lower or 'pred' in col_lower:
                revenue_col = col
            if 'name' in col_lower or 'company' in col_lower:
                name_col = col
            if 'rank' in col_lower:
                rank_col = col
        
        if revenue_col is None and len(df_pred.select_dtypes(include=[np.number]).columns) > 0:
            revenue_col = df_pred.select_dtypes(include=[np.number]).columns[0]
        
        display_cols = []
        if name_col:
            display_cols.append(name_col)
        if revenue_col:
            display_cols.append(revenue_col)
        if rank_col:
            display_cols.append(rank_col)
        
        if revenue_col and name_col:
            df_pred_sorted = df_pred.sort_values(revenue_col, ascending=False).head(20)
            fig = px.bar(df_pred_sorted, x=revenue_col, y=name_col, orientation='h',
                        title=_("Top 20 Predicted Companies 2024", "أفضل 20 شركة متوقعة 2024"),
                        color=revenue_col, color_continuous_scale='viridis')
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=500, font=dict(color='#000000'))
            st.plotly_chart(fig, use_container_width=True)
        elif revenue_col:
            df_pred_sorted = df_pred.sort_values(revenue_col, ascending=False).head(20)
            fig = px.bar(df_pred_sorted, x=revenue_col, y=df_pred_sorted.index, orientation='h',
                        title=_("Top 20 Predictions 2024", "أفضل 20 توقع 2024"),
                        color=revenue_col, color_continuous_scale='viridis')
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=500, font=dict(color='#000000'))
            st.plotly_chart(fig, use_container_width=True)
        
        if display_cols:
            st.dataframe(df_pred[display_cols].head(50), use_container_width=True)
        else:
            st.dataframe(df_pred.head(50), use_container_width=True)
    else:
        st.info(_("2024 predictions file not available", "ملف توقعات 2024 غير متوفر"))
    
    if not data['models'].empty:
        st.subheader(_("Model Performance", "أداء النماذج"))
        df_models = data['models']
        
        model_col = None
        accuracy_col = None
        
        for col in df_models.columns:
            col_lower = col.lower()
            if 'model' in col_lower or 'name' in col_lower:
                model_col = col
            if 'acc' in col_lower or 'score' in col_lower or 'r2' in col_lower:
                accuracy_col = col
        
        if accuracy_col:
            if model_col:
                fig = px.bar(df_models, x=model_col, y=accuracy_col, 
                           title=_("Model Accuracy", "دقة النماذج"),
                           color=accuracy_col, color_continuous_scale='rdylgn')
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=400, xaxis_tickangle=45, font=dict(color='#000000'))
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.bar(df_models, y=accuracy_col, 
                           title=_("Model Accuracy", "دقة النماذج"),
                           color=accuracy_col, color_continuous_scale='rdylgn')
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=400, font=dict(color='#000000'))
                st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df_models, use_container_width=True)
    
    if not data['test'].empty:
        st.subheader(_("Test Predictions", "توقعات الاختبار"))
        df_test = data['test']
        
        actual_col = None
        predicted_col = None
        
        for col in df_test.columns:
            col_lower = col.lower()
            if 'actual' in col_lower or 'true' in col_lower:
                actual_col = col
            if 'pred' in col_lower or 'predict' in col_lower:
                predicted_col = col
        
        if actual_col and predicted_col:
            fig = px.scatter(df_test.head(100), x=actual_col, y=predicted_col,
                           title=_("Actual vs Predicted", "الفعلية مقابل المتوقعة"),
                           labels={actual_col: _("Actual", "فعلية"), predicted_col: _("Predicted", "متوقعة")})
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=500, font=dict(color='#000000'))
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df_test.head(50), use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.header(_("Data Overview", "نظرة عامة"))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(_("Total Years", "إجمالي السنوات"), df['year'].nunique())
    with col2:
        st.metric(_("Unique Companies", "الشركات الفريدة"), df['name'].nunique())
    with col3:
        st.metric(_("Total Revenue", "إجمالي الإيرادات"), f"${df['revenue_mil'].sum()/1000000:,.1f}T")
    with col4:
        st.metric(_("Avg Annual Growth", "متوسط النمو السنوي"), f"{df.groupby('year')['revenue_mil'].mean().pct_change().mean()*100:.1f}%")
    yearly = df.groupby('year').agg({'revenue_mil':'mean','profit_mil':'mean','profit_margin':'mean'}).reset_index()
    fig = make_subplots(rows=3, cols=1, subplot_titles=(
        _("Average Revenue Trend", "اتجاه متوسط الإيرادات"),
        _("Average Profit Trend", "اتجاه متوسط الأرباح"),
        _("Average Margin Trend", "اتجاه متوسط الهامش")
    ))
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['revenue_mil'], name=_("Revenue","الإيرادات")), row=1, col=1)
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['profit_mil'], name=_("Profit","الأرباح")), row=2, col=1)
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['profit_margin'], name=_("Margin","الهامش")), row=3, col=1)
    fig.update_layout(height=700, showlegend=False, plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#000000'))
    st.plotly_chart(fig, use_container_width=True)
    top = df.groupby('name')['revenue_mil'].max().nlargest(15)
    fig2 = px.bar(x=top.values, y=top.index, orientation='h',
                 title=_("Top 15 Companies All Time", "أفضل 15 شركة على الإطلاق"),
                 color=top.values, color_continuous_scale='viridis')
    fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=500, font=dict(color='#000000'))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<hr style="margin: 40px 0; border: none; height: 1px; background: rgba(255,255,255,0.2);">
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 20px;">
    <p style="font-size: 1.2rem; margin-bottom: 10px;"><strong>{_('Fortune 500 Analytics Dashboard', 'لوحة تحليل Fortune 500')}</strong></p>
    <p style="font-size: 1.1rem; margin-bottom: 5px;">{_('Developed by: Mohammad Naser', 'تم التطوير بواسطة: محمد زكريا ناصر')}</p>
    <p style="font-size: 1rem; margin-bottom: 5px;">{_('Data Scientist ', 'عالم بيانات')}</p>
    <p style="font-size: 0.9rem; margin-bottom: 5px;">{_('© 2024 All Rights Reserved', '© 2024 جميع الحقوق محفوظة')}</p>
    <p style="font-size: 0.9rem;">{_('Powered by Streamlit & Plotly', 'بتقنية Streamlit و Plotly')} | 1996-2024</p>
</div>
""", unsafe_allow_html=True)

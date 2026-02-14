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
    page_title="Fortune 500 | Executive Analytics",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS فخم جداً
st.markdown("""
<style>
    /* خطوط فخمة */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }
    
    /* خلفية فخمة جداً */
    .stApp {
        background: linear-gradient(135deg, #0f0c1f 0%, #1a1730 50%, #0f0c1f 100%);
        position: relative;
    }
    
    /* تأثير الجزيئات الذهبية (Gold Particles) */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(212, 175, 55, 0.15) 0%, transparent 20%),
            radial-gradient(circle at 80% 70%, rgba(212, 175, 55, 0.12) 0%, transparent 25%),
            radial-gradient(circle at 40% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(212, 175, 55, 0.1) 0%, transparent 25%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* الكارد الرئيسي الفخم */
    .luxury-card {
        background: rgba(20, 15, 35, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 30px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(212, 175, 55, 0.1) inset,
            0 0 30px rgba(212, 175, 55, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    /* تأثير اللمعة الذهبية على الكارد */
    .luxury-card::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 30%, rgba(212, 175, 55, 0.1), transparent 70%);
        opacity: 0.5;
        pointer-events: none;
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* الهيدر الفخم */
    .luxury-header {
        background: linear-gradient(135deg, rgba(30, 25, 45, 0.95) 0%, rgba(20, 15, 35, 0.98) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 40px;
        padding: 50px 40px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.6),
            0 0 0 2px rgba(212, 175, 55, 0.2) inset,
            0 0 50px rgba(212, 175, 55, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .luxury-header::before {
        content: "FORTUNE 500";
        position: absolute;
        top: 20px;
        right: 40px;
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        font-weight: 900;
        color: rgba(212, 175, 55, 0.15);
        letter-spacing: 5px;
        transform: rotate(90deg);
        transform-origin: right top;
        white-space: nowrap;
    }
    
    .luxury-header::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear

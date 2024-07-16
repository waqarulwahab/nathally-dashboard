import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import datetime, timedelta
from logics.fetch_google_analytics_data import *
from logics.date_range import *
from plots.plots_Google_Ads_Performance import *
from plots.cards import *
import os
from dotenv import load_dotenv

st.sidebar.page_link("main.py", label="Overview", icon="🏠")
st.sidebar.page_link("pages/Google_Ads_Performance.py",       label="Google",       icon="👥", disabled=False)
st.sidebar.page_link("pages/facebook_ads.py",                 label="Facebook",     icon="👥", disabled=False)
st.sidebar.page_link("pages/instagram_data.py",               label="Instagram",    icon="👥", disabled=False)

try:
    # Load environment variables from .env
    load_dotenv()

    # Get the key path from the environment variable
    key_path = os.getenv('KEY_PATH')

    if key_path is None:
        print("Warning: KEY_PATH is not defined in the environment.")

    # Check if all loaded variables are present in the environment
    if not os.environ.get('KEY_PATH'):
        print('Warning: KEY_PATH is not present in the environment.')
    else:
        print('Correctly deploy need to  Users')

    # Initialize Google Analytics 4 client
    client = initialize_ga4_client()
    # client = initialize_ga4_client(key_path)

    if client is None:
        raise ValueError("Failed to initialize GA4 client")
    
    property_id = '323323366'
    
    # client = initialize_ga4_client(key_path)
    dimensions, metrics = get_metadata(client, property_id)


except ValueError as e:
    print(f"ValueError: {e}")
    # Handle the error gracefully

except Exception as e:
    print(f"Error fetching data: {e}")



st.sidebar.divider()
start_date, end_date = date_range()

metrics_dimensions = {
    "engagedSessions": ["audienceName"],
}

try:
    dimensions_total = []
    metrics_total    = ['totalUsers', 'totalRevenue', 'averagePurchaseRevenue']
    total_data_ = fetch_data(client, property_id, dimensions_total, metrics_total, str(start_date), str(end_date))

    selected_dimensions = ['date','dayOfWeek','month','campaignName']
    selected_metrics    = ['advertiserAdClicks', 'advertiserAdImpressions', 'advertiserAdCost', 'advertiserAdCostPerClick',
                           'returnOnAdSpend']
    data_ = fetch_data(client, property_id, selected_dimensions, selected_metrics, str(start_date), str(end_date))
    

    data       = pd.DataFrame(data_)
    total_data = pd.DataFrame(total_data_)

    data['date']      = pd.to_datetime(data['date'], format='%Y%m%d')
    data['date']      = data['date'].dt.strftime('%Y-%m-%d')
    data['dayOfWeek'] = pd.to_datetime(data['date']).dt.day_name()
    data['month']     = pd.to_datetime(data['date']).dt.month_name()


    total_compaigns        = data['campaignName'].nunique()
    returnOnAdSpend_Values = data['returnOnAdSpend']
    

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        title = "Total de Usuários"
        cards(title , int(total_data['totalUsers'].nunique()))
    with col2:
        title = "Total de Campanhas"
        cards(title , total_compaigns)
    with col3:
        title = "Retorno sobre Investimento em Anúncios"
        cards(title , int(returnOnAdSpend_Values.sum()))
    with col4:
        title = "Receita Total"
        cards(title , int(total_data['totalRevenue'].nunique()))
    with col5:
        title = "Receita Média por Compra"
        cards(title , int(total_data['averagePurchaseRevenue'].nunique()))    

    st.divider()
    

    google_ads_impressions_clicks(data)

    google_ads_cost_perclick(data)

    st.divider()

    col1, col2 = st.columns([1,1])
    with col1:
        advertiserAdCostPerClick(data)
    with col2:
        returnOnAdSpend(data)

except Exception as e:
    st.error(f"Error fetching data: {e}")



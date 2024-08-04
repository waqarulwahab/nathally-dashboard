import streamlit as st
import requests
from datetime import datetime, timedelta

def fetch_instagram_insights(user_id, access_token, start_date, end_date, metrics, period, lifetime):
    url = f"https://graph.facebook.com/v12.0/{user_id}/insights"

    params = {
        'access_token': access_token,
        'metric': ','.join(metrics),
        'since':    start_date,
        'until':    end_date,
        'period':   period,
        'lifetime': lifetime,
    }
    response = requests.get(url, params=params)
    response_json = response.json()

    if 'error' in response_json:
        st.error(f"Error: {response_json['error']['message']}")
        st.json(response_json)  # Display the full response for debugging
        return None
    return response_json


def fetch_instagram_insights_with_total_values(user_id, access_token):
    url = f"https://graph.facebook.com/v12.0/{user_id}/insights"

    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)


    metrics = ['likes']
    params = {
        'access_token': access_token,
        'metric': ','.join(metrics),
        'since':    start_date,
        'until':    end_date,
        'period':   'day',
        'metric_type': 'total_value'  # Add this parameter
    }
    response = requests.get(url, params=params)
    response_json = response.json()

    if 'error' in response_json:
        st.error(f"Error: {response_json['error']['message']}")
        st.json(response_json)  # Display the full response for debugging
        return None
    return response_json



def get_valid_metrics_by_days():
    valid_metrics = [
            'impressions', 'reach', 'profile_views', 'follower_count',
            'email_contacts', 'phone_call_clicks', 'text_message_clicks',
            'get_directions_clicks', 'website_clicks',
            ]
    return valid_metrics
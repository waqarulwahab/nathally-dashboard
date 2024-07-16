import streamlit as st
import pandas as pd
from facebook_business.api import FacebookAdsApi

from logics.fetch_facebook import *
from logics.date_range import *

from plots.plots_facebook import *
from plots.cards import *
from plots.plots_ads_account import *
from logics.fetch_adaccounts import *
from logics.date_range import *


st.sidebar.page_link("main.py", label="Overview", icon="🏠")
st.sidebar.page_link("pages/Google_Ads_Performance.py",       label="Google",       icon="👥", disabled=False)
st.sidebar.page_link("pages/facebook_ads.py",                 label="Facebook",     icon="👥", disabled=False)
st.sidebar.page_link("pages/instagram_data.py",               label="Instagram",    icon="👥", disabled=False)

page_access_token    = st.secrets["access_tokens"]["page_access_token"]
user_access_token    = st.secrets["access_tokens"]["user_access_token"]
page_id              = st.secrets["facebook"]["page_id"]
adaccount_account_id = st.secrets["adaccount"]["adaccount_account_id"]
adaccount_id         = st.secrets["adaccount"]["adaccount_id"]

# Initialize the Facebook API
FacebookAdsApi.init(access_token= page_access_token)

st.sidebar.divider()
start_date, end_date = date_range()
selected_range       = date_range_for_ads()


try:
    page_insights = get_page_insights(page_id, str(start_date), str(end_date))
    dates = [datetime.strptime(page_insights[0]["values"][i]["end_time"][:10], "%Y-%m-%d").strftime("%Y-%m-%d") for i in range(len(page_insights[0]["values"]))]

    page_post_engagements                 = [data["value"] for data in page_insights[0]["values"]]
    page_impressions                      = [data["value"] for data in page_insights[1]["values"]]
    page_impressions_unique               = [data["value"] for data in page_insights[2]["values"]]

    page_fans                             = [data["value"] for data in page_insights[3]["values"]]
    unique_page_fan                       = list(set(page_fans))[0]

    page_follows                          = [data["value"] for data in page_insights[4]["values"]]
    page_follows                          = pd.DataFrame(page_follows)

    page_views                            = [data["value"] for data in page_insights[5]["values"]]
    page_views                            = pd.DataFrame(page_views)

    page_negative_feedback_unique         = [data["value"] for data in page_insights[6]["values"]]
    page_negative_feedback_unique         = pd.DataFrame(page_negative_feedback_unique)

    page_impressions_viral                = [data["value"] for data in page_insights[7]["values"]]
    page_impressions_viral                = pd.DataFrame(page_impressions_viral)

    page_fan_adds_by_paid_non_paid_unique = [data["value"] for data in page_insights[8]["values"]]
    page_fan_adds_by_paid_non_paid_unique = pd.DataFrame(page_fan_adds_by_paid_non_paid_unique)

    page_daily_follows_unique             = [data["value"] for data in page_insights[9]["values"]]
    page_daily_follows_unique             = pd.DataFrame(page_daily_follows_unique)

    page_fan_adds_by_paid_non_paid_unique = [data["value"] for data in page_insights[8]["values"]]
    page_fan_adds_by_paid_non_paid_unique = pd.DataFrame(page_fan_adds_by_paid_non_paid_unique)


    page_daily_follows_unique             = [data["value"] for data in page_insights[9]["values"]]
    page_daily_unfollows_unique           = [data["value"] for data in page_insights[10]["values"]]

    page_impressions_by_age_gender_unique = [data["value"] for data in page_insights[11]["values"]]
    page_impressions_by_age_gender_unique = pd.DataFrame(page_impressions_by_age_gender_unique)

    page_impressions_organic_unique_v2    = [data["value"] for data in page_insights[12]["values"]]
    page_impressions_paid                 = [data["value"] for data in page_insights[13]["values"]]
    post_reactions                        = [data["value"] for data in page_insights[14]["values"]]
    page_fans_country                     = [data["value"] for data in page_insights[15]["values"]]
    page_fan_adds                         = [data["value"] for data in page_insights[16]["values"]]
    page_fan_removes                      = [data["value"] for data in page_insights[17]["values"]]



    ada_account  = get_ad_accounts(user_access_token, adaccount_account_id)
    ads_insights = get_insights_from_ada_account(user_access_token, adaccount_id, selected_range)

    ads_insights = [{
        'ad_name': ad.get('ad_name'),
        'spend': ad.get('spend'),
        'social_spend': ad.get('social_spend'),
        'reach': ad.get('reach'),
        'impressions': ad.get('impressions'),
        'cpm': ad.get('cpm'),
        'cpp': ad.get('cpp'),
        'ctr': ad.get('ctr'),
        'clicks': ad.get('clicks'),
        'conversion_values': ad.get('conversion_values'),
        'conversions': sum(int(conv.get('value', 0)) for conv in ad.get('conversions', [])),
    } for ad in ads_insights['data'] if 'ad_name' in ad]
    ads_insights = pd.DataFrame(ads_insights)

    group_ads_details = group_by_ad_name(ads_insights)
    group_ads_details['roi'] = round((group_ads_details['conversions'] / group_ads_details['spend']) * 100,2) # Calculate ROI
    ad_names    = group_ads_details['ad_name']
    roi         = group_ads_details['roi']
    spend       = group_ads_details['spend']
    conversions = group_ads_details['conversions']


    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        title = "Total de Visualizações de Página"
        cards(title , page_views.sum()[0])

    with col2:
        title = "Total de Seguidores"
        cards(title , page_follows.sum()[0])
    with col3:
        title = "Total de Curtidas"
        cards(title , unique_page_fan)
    with col4:
        title = "Feedbacks Negativos"
        cards(title , page_negative_feedback_unique.sum()[0])
    with col5:
        title = "Impressões Virais"
        cards(title , page_impressions_viral.sum()[0])


    st.divider()

    if page_insights:
        page_impression_engagement(page_post_engagements, page_impressions, page_impressions_unique, dates)

        col1, col2 = st.columns([1,1])
        with col1:
            page_fan_adds_by_paid_unpaid_unique(page_fan_adds_by_paid_non_paid_unique, dates)
        with col2:
            page_daily_follows_unfollow(page_daily_follows_unique, page_daily_unfollows_unique, dates)

        try:
            col1, col2 = st.columns([1,1])
            with col1:
                page_impressions_by_age_gender_male(page_impressions_by_age_gender_unique, dates)
            with col2:
                page_impressions_by_age_gender_female(page_impressions_by_age_gender_unique, dates)
        except:
            pass

        page_impressions_organic_paid(page_impressions_organic_unique_v2, page_impressions_paid,  dates)
        st.divider()

        col1, col2 = st.columns([1,1])
        with col1:
            page_fans_country_plot(page_fans_country, dates)
        with col2:
            page_actions_post_reactions(post_reactions, dates)
        
        page_fan_adds_remove(page_fan_adds,page_fan_removes, dates)

        st.divider()






        try:
            cpm_cpp_ctr_clicks(group_ads_details)
            spend_on_ads(group_ads_details)

            col1, col2 = st.columns([1,1])
            with col1:
                roi_by_ad_names(ad_names, roi)
            with col2:
                total_roi_spend_conv_pie_charts(roi, spend, conversions)
                

            ads_stacked_bar_chart(ad_names, roi, spend, conversions, selected_range)
        except:
            pass

    else:
        st.write("No insights data available")

except Exception as e:
    st.error(f"Error fetching page insights: {e}")

except:
    st.warning("No Data Found for selected range")
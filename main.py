import streamlit as st
from pages.User_Engagement_and_Activity import *
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from logics.date_range import *

st.set_page_config(layout="wide")
    
def main():
    # key_path = 'credentials.json'
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


        client = initialize_ga4_client()
        # client = initialize_ga4_client(key_path)

        if client is None:
            raise ValueError("Failed to initialize GA4 client")


        property_id = '323323366'

        dimensions, metrics = get_metadata(client, property_id)

    except ValueError as e:
        st.write(f"ValueError: {e}")
        # Handle the error gracefully

    except Exception as e:
        st.write(f"Error fetching data: {e}")


    # Path to your Google icon image
    google_icon_path = "Logo-google-icon-PNG.png"

    # # Display the icon with a link in the sidebar
    # st.sidebar.image(google_icon_path, width=30)
    # st.sidebar.markdown("[Google](pages/Google_Ads_Performance.py)")

    # # # Optional: Add a label below the icon
    # # st.sidebar.write("Google")



    st.sidebar.page_link("main.py", label="Overview", icon="🏠")
    st.sidebar.page_link("pages/Google_Ads_Performance.py",       label="Google",       icon="👥", disabled=False)
    st.sidebar.page_link("pages/facebook_ads.py",                 label="Facebook",     icon="👥", disabled=False)
    st.sidebar.page_link("pages/instagram_data.py",               label="Instagram",    icon="👥", disabled=False)




    st.sidebar.divider()
    start_date, end_date = date_range()

    try:

        selected_dimensions = ['date','dayOfWeek','operatingSystem', 'browser', 'deviceCategory', 'country', 'continent', 'sessionSourceMedium']
        selected_metrics    = ['sessions', 'engagedSessions','averageSessionDuration','engagementRate',
                                'bounceRate', 'eventCount', 'dauPerMau','wauPerMau', 'screenPageViews']

        rose_pie_dimensions = ['source']
        rose_pie_metrics    = ['activeUsers', 'totalUsers']

        eventCount_dimensions = ['eventName']
        eventCount_metrics    = ['eventCount', 'eventCountPerUser']

        sunbrust_dimensions = ['operatingSystem', 'browser', 'deviceCategory']
        sunbrust_metrics    = ['sessions']

        data_            = fetch_data(client, property_id, selected_dimensions, selected_metrics, str(start_date), str(end_date))
        rose_pie_data_   = fetch_data(client, property_id, rose_pie_dimensions, rose_pie_metrics, str(start_date), str(end_date))
        eventCount_data_ = fetch_data(client, property_id, eventCount_dimensions, eventCount_metrics, str(start_date), str(end_date))
        sunbrust_data_   = fetch_data(client, property_id, sunbrust_dimensions, sunbrust_metrics, str(start_date), str(end_date))


        data          = pd.DataFrame(data_)
        rose_pie      = pd.DataFrame(rose_pie_data_)
        eventCount    = pd.DataFrame(eventCount_data_)
        sunbrust_data = pd.DataFrame(sunbrust_data_)

        data['date']      = pd.to_datetime(data['date'], format='%Y%m%d')
        data['date']      = data['date'].dt.strftime('%Y-%m-%d')
        data['dayOfWeek'] = pd.to_datetime(data['date']).dt.day_name()
        # Clean data: Convert sessions to numeric, coerce errors to NaN
        data['sessions'] = pd.to_numeric(data['sessions'], errors='coerce')
        data = data.dropna(subset=['sessions'])

        user_engagement_activity(data, rose_pie, eventCount, sunbrust_data)
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")


if __name__ == '__main__':
    main()






















# if selected_dimensions and selected_metrics:
#     try:
#         # Fetch data from GA4
#         data = fetch_data(client, property_id, selected_dimensions, selected_metrics, str(start_date), str(end_date))
        
#         # Convert data types
#         for dim in selected_dimensions:
#             data[dim] = data[dim].astype(str)
#         for met in selected_metrics:
#             data[met] = pd.to_numeric(data[met], errors='coerce')

#         # Display the dataframe
#         st.dataframe(data)
        
#         # Generate and display graphs
#         for metric in selected_metrics:
#             chart = alt.Chart(data).mark_bar().encode(
#                 x=alt.X(selected_dimensions[0], sort='-y'),
#                 y=metric,
#                 tooltip=[selected_dimensions[0], metric]
#             ).interactive()
            
#             st.altair_chart(chart, use_container_width=True)
#     except Exception as e:
#         st.error(f"Error fetching data: {e}")
# else:
#     st.info("Please select at least one dimension and one metric.")








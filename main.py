import streamlit as st
from logics.date_range import date_range
from pages.User_Engagement_and_Activity import user_engagement_activity
from logics.export_data import export_data
import pandas as pd


st.set_page_config(layout="wide")


def main():
    st.sidebar.page_link("main.py", label="Overview", icon="🏠")
    st.sidebar.page_link("pages/Google_Ads_Performance.py",       label="Google",       icon="👥", disabled=False)
    st.sidebar.page_link("pages/facebook_ads.py",                 label="Facebook",     icon="👥", disabled=False)
    st.sidebar.page_link("pages/instagram_data.py",               label="Instagram",    icon="👥", disabled=False)

    st.sidebar.divider()
    start_date, end_date = date_range()


    export_button = st.sidebar.toggle("Export_Data")
    if export_button:
        export_data(start_date, end_date)


    user_engagement_activity(start_date, end_date)


    uploaded_file = st.sidebar.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                df.to_csv('uploaded_data.csv')
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
                df.to_excel('uploaded_data.xlsx')
            st.sidebar.success("File successfully uploaded and read!")
            st.sidebar.page_link("pages/import_data.py",  label="import Data",    icon="👥", disabled=False)
        except Exception as e:
            st.error(f"Error: {e}")






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








import streamlit as st
import pandas as pd
import openpyxl


st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True
)
st.markdown("<h1><i class='fas fa-chart-line'></i> Company Stats</h1>", unsafe_allow_html=True)

# st.title("  Comapany Stats")

Data_selector = st.sidebar.selectbox(
    'Select a Data set to be viewed -->',
    (' ','Student Details', 'Company Details', 'Company Requirements'), 
    help='Select a Dataset to be displayed and to visualize',
    placeholder= 'Choose an option'
)

df = pd.read_excel('Student_data.xlsx',sheet_name='Sheet1')

# df['average_marks'] = df[['College_aggrigate_percentage', 'SSLC_percentage', 'HSC_persentage']].mean(axis=0)

# st.dataframe(df, column_config={
#     'average_marks': st.column_config.LineChartColumn('Average percentage', y_min=0, y_max=100)
# })


st.dataframe(
    df,
    hide_index=True,
)


with st.popover('sett'):
    st.markdown('hello')
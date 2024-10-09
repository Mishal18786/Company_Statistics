import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import documents
from documents import scope, dataset_urls, crediential
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True
)
st.markdown("<h1><i class='fas fa-chart-line'></i> Company Stats</h1>", unsafe_allow_html=True)

Data_selector = st.sidebar.selectbox(
    'Select a Data set to be viewed -->',
    (' ','Student Details', 'Company Details', 'Company Requirements'), 
    help='Select a Dataset to be displayed and to visualize',
    placeholder= 'Choose an option'
)

@st.cache_data
def connect_to_sheet(url):
    try:
        client = gspread.authorize(crediential)
        sheet = client.open_by_url(url).sheet1
        return sheet.get_all_values() #raw data
    
    except Exception as er:
        st.error(f'Error Fetching Data {er}')
        return None

# Loading the data
@st.cache_data
def process_data(data):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    return df



if Data_selector == ' ':

    st.subheader('Welcome To Company Statistics',help='You can select a dataset from the menu')
    st.markdown(documents.Business_understanding)

    st.subheader('Data Collection')  
    st.markdown(documents.Data_collected)

    with st.expander('Student Table Details', expanded=False):
        st.markdown(documents.Student_table)

    with st.expander('Company Table Details', expanded=False):
        st.markdown(documents.company_details)

    with st.expander('Company Requirment Table Details', expanded=False):
        st.markdown(documents.company_requirments)

    st.subheader('Data Cleaning')
    with st.expander('Data Cleaned', expanded=False):
        st.markdown(documents.data_cleaning)

    st.subheader('Data Analysis')
    with st.expander('Data Analysis', expanded=False):
        st.markdown(documents.eda1)
        st.markdown(documents.eda2)

    st.subheader('Feature Engineering')
    with st.expander('Feature Engineering', expanded=False):
        st.markdown(documents.feature_engineering)

    # with st.expander('Model Buildiing', expanded=False):
    #     pass

    # with st.expander('Deployment', expanded=False):
    #     pass


if Data_selector != ' ':

    raw_data = None
    if Data_selector in dataset_urls and Data_selector:
        raw_data = connect_to_sheet(dataset_urls[Data_selector])

    st.subheader(f"{Data_selector} ")

    if raw_data:
        df = process_data(raw_data)

        with st.expander(f'{Data_selector} Data Viewer'):
            st.dataframe(df)
        
        st.write(f'Number of Rows: {df.shape[0]}')
        st.write(f'Number of Columns {df.shape[1]}')

        with st.expander('Data Summary', expanded=False):
            st.subheader('Data Summary')
            st.dataframe(df.describe().T)

        with st.expander('Filter Data', expanded=False):
            st.subheader("Filter Data")
            columns = df.columns.tolist()
            selected_column = st.selectbox("Select column to filter by", columns)
            unique_values = df[selected_column].unique()
            selected_value = st.selectbox("Select value", unique_values)      

            filtered_df = df[df[selected_column] == selected_value]
            st.write(filtered_df)
            st.write(f' Number Of ROWS {filtered_df.shape[0]}')    

        if Data_selector == 'Student Details':

            student_visualization = st.sidebar.selectbox('Select a Data set to be viewed -->',
            (' ','Data Visulization', 'Model Building'), 
            help='Select an Option to be displayed and to visualize',
            placeholder= 'Choose an option')

            if student_visualization == 'Data Visulization':

                st.header('Data Visulization')

                with st.expander('Custom Plots', expanded=False):
                    pass

                with st.expander('Gender Distribution ', expanded=False):
                    #st.write('Gender Distribution')
                    fig, ax = plt.subplots()
                    sns.countplot(x = 'Gender', data=df)
                    ax.set_xlabel('Gender')
                    ax.set_ylabel('Count of Gender')
                    plt.xticks(rotation = 90)
                    st.pyplot(fig)

                with st.expander('Course Selection', expanded=False):
                    #st.write('Gender Distribution')
                    fig, ax = plt.subplots()
                    sns.countplot(x = 'Course_enrolled', data=df)
                    ax.set_xlabel('Course enrolled by students')
                    ax.set_ylabel('Count of Students')
                    plt.xticks(rotation = 90)
                    st.pyplot(fig)


                X = df[['Gender', 'Age', 'Field_of_study', 'Work_experience',
                    'College_aggrigate_percentage', 
                    'SSLC_percentage', 'HSC_persentage']]
                y = df['Course_enrolled']


                X = pd.get_dummies(X, columns=['Gender', 'Field_of_study'], drop_first=True)


                le = LabelEncoder()
                y_encoded = le.fit_transform(y)


                X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)


                scaler = StandardScaler()
                X_train = scaler.fit_transform(X_train)
                X_test = scaler.transform(X_test)

                params = {
                    'C': [0.1, 1.0, 10],
                    'penalty': ['l2'],
                    'solver': ['liblinear', 'lbfgs']
                }


                st.title('Model Building')

                model_options = st.selectbox("Select a model", ["Logistic Regression", "Random Forest", "Support Vector Machine"])

                if st.button('Run Model'):
                    if model_options == "Logistic Regression":
                        params = {
                            'C': [0.1, 1.0, 10],
                            'penalty': ['l2'],
                            'solver': ['liblinear', 'lbfgs']
                        }
                        model = LogisticRegression(max_iter=1000)

                    elif model_options == "Random Forest":
                        params = {
                            'n_estimators': [50, 100, 200],
                            'max_depth': [None, 10, 20, 30],
                            'min_samples_split': [2, 5, 10]
                        }
                        model = RandomForestClassifier()

                    elif model_options == "Support Vector Machine":
                        params = {
                            'C': [0.1, 1.0, 10],
                            'kernel': ['linear', 'rbf']
                        }
                        model = SVC()

                    # Perform Grid Search
                    grid_search = GridSearchCV(estimator=model, param_grid=params, scoring='accuracy', cv=5)

                    # Fit the model
                    grid_search.fit(X_train, y_train)

                    # Make predictions
                    y_pred = grid_search.predict(X_test)

                    # Calculate accuracy
                    accuracy = accuracy_score(y_test, y_pred)

                    # Display results
                    st.write(f'Selected Model: {model_options}')
                    st.write(f'Best parameters: {grid_search.best_params_}')
                    st.write(f'Accuracy: {accuracy:.2f}')
            
        








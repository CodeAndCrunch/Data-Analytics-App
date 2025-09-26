# Import Libraries
import pandas as pd
import plotly.express as px
import streamlit as st
import time

st.set_page_config(
    page_title='Analytics Portal',
    page_icon='📊'
)

#title
col1, col2, col3 = st.columns([1.5, 5, 1.5]) # Adjust ratios as needed
with col2:
   st.title(':rainbow[Data Analytics Portal]',)
   st.divider()

#header
st.subheader(':rainbow[Explore and Visualize Your Data with Ease]',divider="rainbow")

#fileUploader
file = st.file_uploader('Drop csv or excel file',type=['csv','xlsx'])

#FileInsights
if(file!=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.info('File is uploaded successfully',icon="🔥")

    #BasicInsights
    st.subheader(':rainbow[Basic Insights of the Dataset]', divider="rainbow")

    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Top & Bottom Rows", "Data Types", "Columns"])

    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statistical Summary]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))

        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':gray[Data types of Columns]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(':gray[Available Column Names in Dataset]')
        st.write(list(data.columns))


    #CoumnValueCalculator
    st.subheader(':rainbow[Column Values To Count]', divider='rainbow')
    with st.expander('Value Count'):
        col1, col2 = st.columns(2)

        with col1:
            column = st.selectbox('Choose Column', options=list(data.columns))

        with col2:
            toprows = st.number_input('Top rows', min_value=1,step=1)

        count = st.button('Count')
        if(count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)

            #Visualization
            st.subheader(':gray[Visualization]', divider='gray')

            st.caption(":red[Bar Chart]")
            fig = px.bar(data_frame=result, x=column, y='count', text='count', color='count',template="ygridoff")
            st.plotly_chart(fig)

            st.caption(":red[Line Graph]")
            fig = px.line(data_frame=result, x=column, y='count', text='count', template="ygridoff")
            st.plotly_chart(fig)

            st.caption(":red[Pie Chart]")
            fig = px.pie(data_frame=result, names=column, values='count',template='presentation')
            st.plotly_chart(fig)

    #GroupBy       
    st.subheader(':rainbow[Groupby - Simplify Your Analysis]', divider='rainbow')
    st.write('The groupby() summarizes data by grouping it based on categories and applying aggregation functions.')


    
    with st.expander('Group By Columns'):
        col1, col2, col3 = st.columns(3)

        with col1:
            groupby_cols = st.multiselect('Choose column to groupby', options=list(data.columns))

        with col2:
            operation_col = st.selectbox('Operation Column', options=list(data.columns))

        with col3:
            operation = st.selectbox('Choose Operation', options=['sum', 'max', 'min', 'mean', 'median', 'count'])

        if groupby_cols:
            try:
                result = data.groupby(groupby_cols).agg(
                    newcol=(operation_col, operation)
                ).reset_index()

                st.dataframe(result)

            except Exception as e:
                st.error(f"Error during aggregation: {e}")

            #Visualization
            if 'result' in locals():
                st.subheader('Data Visualization', divider='gray')
                graphs = st.selectbox('Choose Graphs', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])

                numeric_cols = result.select_dtypes(include='number').columns.tolist()
                all_cols = result.columns.tolist()

                if graphs == 'line':
                    x_axis = st.selectbox('Choose X axis', options=all_cols)
                    y_axis = st.selectbox('Choose Y axis', options=numeric_cols)
                    color = st.selectbox('Choose Color', options=[None] + all_cols)
                    facet_col = st.selectbox('Choose additional columns', options=[None] + all_cols)
                    fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, markers='o')
                    st.plotly_chart(fig)

                elif graphs == 'bar':
                    x_axis = st.selectbox('Choose X axis', options=all_cols)
                    y_axis = st.selectbox('Choose Y axis', options=numeric_cols)
                    color = st.selectbox('Choose Color', options=[None] + all_cols)
                    facet_col = st.selectbox('Choose additional columns', options=[None] + all_cols)
                    fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                    st.plotly_chart(fig)

                elif graphs == 'scatter':
                    x_axis = st.selectbox('Choose X axis', options=numeric_cols)
                    y_axis = st.selectbox('Choose Y axis', options=numeric_cols)
                    color = st.selectbox('Choose Color', options=[None] + all_cols)
                    size = st.selectbox('Choose Size', options=[None] + numeric_cols)
                    fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
                    st.plotly_chart(fig)

                elif graphs == 'pie':
                    names = st.selectbox('Choose Labels (Names)', options=all_cols)
                    values = st.selectbox('Choose Values', options=numeric_cols)
                    fig = px.pie(data_frame=result, names=names, values=values)
                    st.plotly_chart(fig)

                elif graphs == 'sunburst':
                    path = st.multiselect('Choose Path', options=all_cols)
                    if path:
                        fig = px.sunburst(data_frame=result, path=path, values='newcol')
                        st.plotly_chart(fig)
                    else:
                        st.warning("Please select at least one column for the sunburst path.")
            else:
                st.info("Please perform a groupby operation to enable visualizations.")



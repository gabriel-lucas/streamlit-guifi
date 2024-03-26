import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to load the uploaded file
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    data['Fecha factura'] = pd.to_datetime(data['Fecha factura'], format='%d/%m/%Y')
    # Convert 'Total' and 'Importe de deuda' to numeric
    data['Total'] = pd.to_numeric(data['Total'].str.replace(',','.'), errors='coerce')
    data['Importe de deuda'] = pd.to_numeric(data['Importe de deuda'].str.replace(',','.'), errors='coerce')
    print( "Total ",data['Total'] )
    print( "Importe de deuda ",data['Importe de deuda'] )
    return data

# Function to filter data based on selected clients and date range
def filter_data(data, selected_clients, start_date1, end_date1, invoice_state):
    filtered_data = data[data['Cliente'].isin(selected_clients)]
    start_date = pd.to_datetime(start_date1, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date1, format='%Y/%m/%d')
    filtered_data = filtered_data[(filtered_data['Fecha factura'] >= start_date) & (filtered_data['Fecha factura'] <= end_date)]
    filtered_data = filtered_data[filtered_data['Estado'] == invoice_state]
    return filtered_data

# Main Streamlit app
st.title('Invoice Analysis Dashboard')

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload your invoices file", type=['csv'])

if uploaded_file is not None:
    data = load_data(uploaded_file)
    st.write(data.head())

    # Select multiple clients
    selected_clients = st.sidebar.multiselect("Select clients", options=data['Cliente'].unique())

    # Date range filter
    start_date, end_date = st.sidebar.date_input("Select date range", [data['Fecha factura'].min(), data['Fecha factura'].max()])

    # Invoice state filter
    invoice_state = st.sidebar.selectbox("Select invoice state", options=data['Estado'].unique())

    if st.sidebar.button("Filter"):
        filtered_data = filter_data(data, selected_clients, start_date, end_date, invoice_state)
        st.write(filtered_data)
        
        # Create a bar chart with Plotly
        fig = go.Figure(data=[
            go.Bar(
                x=filtered_data['Fecha factura'],
                y=filtered_data['Total'] - filtered_data['Importe de deuda'],
                name='Paid Amount',
                marker_color='green'
            ),
            go.Bar(
                x=filtered_data['Fecha factura'],
                y=filtered_data['Importe de deuda'],
                name='Debt Amount',
                marker_color='red'
            )
        ])
        
        # Set axis labels
        fig.update_layout(
            xaxis_title="Fecha factura",
            yaxis_title="€",
            title="Invoice Visualization"
        )
        
        st.plotly_chart(fig)
        
        

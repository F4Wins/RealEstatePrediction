import streamlit as st
import pandas as pd
import time
from utils.Utils import Utils

# --------------------------------------------------------------------------------

st.set_page_config(layout="wide")

result_model_one = None
result_model_two = None
utils = Utils()

# --------------------------------------------------------------------------------

st.header('DSG case study: Forecasting property prices based on hybrid models')

st.subheader('Model evaluation and comparison')

st.text('Chose models to compare: ')

col1, col2 = st.columns(2)

with col1:
    name_model_one = 'GBR + RFR'
    name_model_one = st.selectbox('Model 1',
                                  ('GBR + RFR', 'Ridge + Lasso', 'Linear Regression', 'Lasso', 'GBR'), key='model_one')

    model_one = utils.get_model(name=name_model_one)

with col2:
    name_model_two = 'GBR + RFR'
    name_model_two = st.selectbox('Model 2',
                                  ('GBR + RFR', 'Ridge + Lasso', 'Linear Regression', 'Lasso', 'GBR'), key='model_two')
    model_two = utils.get_model(name=name_model_two)


with st.expander('Data entry of the property:'):
    input_data = utils.build_user_input()
    user_data = utils.process_input(input_data)


if st.button('Calculate', key='calculate'):
    with st.spinner('processing ...'):
        time.sleep(1)
        result_model_one = int((model_one.predict(user_data)))
        result_model_two = int((model_two.predict(user_data)))

if result_model_one and result_model_two != None:

    st.header('Prediction:')
    st.success('Price was calculated:')
    col3, col4 = st.columns(2)

    with col3:
        st.subheader(name_model_one + ':')

        diff = result_model_one - result_model_two

        if diff > 0:
            metric_result = '+' + str(diff)
        else:
            metric_result = str(diff)

        diff_percent = round(((result_model_one - result_model_two) /
                              result_model_one) * 100, 2)

        st.info(str(result_model_one) + '€')
        st.metric(label='Difference: ' + name_model_one + ' to ' + name_model_two,
                  value=metric_result + ' €', delta=str(diff_percent) + ' %')

    with col4:
        metric_result = ''
        st.subheader(name_model_two + ':')
        st.info(str(result_model_two) + '€')

        diff = result_model_two - result_model_one

        if diff > 0:
            metric_result = '+' + str(diff)
        else:
            metric_result = str(diff)

        diff_percent = round(((result_model_two - result_model_one) /
                              result_model_two) * 100, 2)

        st.metric(label='Difference: ' + name_model_two + ' to ' + name_model_one,
                  value=metric_result + ' €', delta=str(diff_percent) + ' %')

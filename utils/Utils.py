import streamlit as st
import pandas as pd
from data.models.Model import Model


class Utils():

    def __init__(self) -> None:
        pass

    def get_model(self, name):

        if name == 'GBR + RFR':
            model_name = 'gbr_rfg_model'
        elif name == 'Ridge + Lasso':
            model_name = 'lasso_ridge_model'
        elif name == 'Linear Regression':
            model_name = 'lr_model'
        elif name == 'GBR':
            model_name = 'gbr_model'
        else:
            model_name = 'lasso_model'

        model = Model(model_name)
        return model

    def build_user_input(self):

        expansion_stage = st.number_input(
            'Please enter the number of floors?', value=2.0,  min_value=1.0, max_value=2.5, step=0.5, format="%.1f", key='expansion')

        st.write('----')

        year_of_build = int(st.number_input(
            'In which year was the property built?', value=2000, min_value=1900, max_value=2023, key='year_of_build'))

        st.write('----')

        eg_qm = st.number_input('Number of quardratmeters on the ground floor?', min_value=1,
                                max_value=2000, value=100, key='eg_qm')

        st.write('----')

        quality_of_the_property = st.radio('What is the first impression of the quality when viewing the property?', [
            'poor', 'average', 'good', 'perfect'], key='quality_property')

        st.write('----')

        total_state_building = st.radio('What is the overall condition of the property?', [
            'really poor', 'poor', 'average', 'good', 'perfect'], key='state_property')

        st.write('----')

        property_qm = st.number_input(
            'How many square metres does the entire property have?', value=500, min_value=0, max_value=10000, key='property_qm')

        st.write('----')

        basement_height = st.radio('What is the ceiling height in the basement?', [
            'no basement', '< 1.75m', '~ 1.75m', '~ 2.0m', '~ 2.25m', '> 2.50m'], key='basement_height')

        st.write('----')

        gradient = st.radio('Is your property on a slope?', [
                            'barely', 'medium', 'strong'], key='gradient')

        st.write('----')

        st.text('Has the property been renovated?')
        check_renovated = st.checkbox('yes')

        if check_renovated:
            renovated = int(st.number_input('In which year did the renovation take place?', value=2000,
                            min_value=1900, max_value=2023, key='year_of_rennovation'))
        else:
            renovated = year_of_build

        st.write('----')

        year_of_sale = int(st.number_input('In which year was the property last sold?', value=2000,
                                           min_value=1900, max_value=2023, key='year_of_last_sale'))

        st.write('----')

        living_qm = st.number_input(
            'What is the square metre of living space?', min_value=100, max_value=10000, value=200, key='house_qm')

        st.write('----')

        # besonders familienverkauf always 0
        special_features_family_sale = 0

        special_features_pool = st.selectbox(
            'Does the property have a pool?', ['yes', 'no'], key='pool')

        st.write('----')

        location = st.selectbox(
            'In which city is the flat located?', ['heilbronn', 'stuttgart', 'berlin'], key='location')

        st.write('----')

        input_data = [
            expansion_stage, year_of_build, eg_qm, quality_of_the_property, total_state_building, property_qm, basement_height, gradient,
            renovated, year_of_sale, living_qm, special_features_family_sale, special_features_pool,
            location]

        return input_data

    def process_input(self, input_data) -> pd.DataFrame:

        quality_of_the_property = input_data[3]
        if quality_of_the_property == 'poor':
            quality_of_the_property = 0
        elif quality_of_the_property == 'average':
            quality_of_the_property = 1
        elif quality_of_the_property == 'good':
            quality_of_the_property = 2
        elif quality_of_the_property == 'perfect':
            quality_of_the_property = 3

        input_data[3] = quality_of_the_property

        total_state_building = input_data[4]
        if total_state_building == 'really poor':
            total_state_building = 0
        elif total_state_building == 'poor':
            total_state_building = 1
        elif total_state_building == 'average':
            total_state_building = 2
        elif total_state_building == 'good':
            total_state_building = 3
        elif total_state_building == 'perfect':
            total_state_building = 4
        input_data[4] = total_state_building

        basement_height = input_data[6]
        if basement_height == 'no basement':
            basement_height = 0
        elif basement_height == '< 1.75m':
            basement_height = 1
        elif basement_height == '~ 1.75m':
            basement_height = 2
        elif basement_height == '~ 2.0m':
            basement_height = 3
        elif basement_height == '~ 2.25m':
            basement_height = 4
        elif basement_height == '> 2.50m':
            basement_height = 5
        input_data[6] = basement_height

        gradient = input_data[7]
        if gradient == 'barely':
            gradient = 0
        elif gradient == 'medium':
            gradient = 1
        elif gradient == 'strong':
            gradient = 2
        input_data[7] = gradient

        special_features_pool = input_data[12]
        if special_features_pool == 'yes':
            special_features_pool = 1
        else:
            special_features_pool = 0
        input_data[12] = special_features_pool

        location = input_data[13]

        location_heilbronn = 0
        location_stuttgart = 0
        location_berlin = 0

        if location == 'heilbronn':
            location_heilbronn = 1
        elif location == 'stuttgart':
            location_stuttgart = 1
        elif location == 'berlin':
            location_berlin = 1

        input_data[13] = location_heilbronn

        input_data.append(location_stuttgart)
        input_data.append(location_berlin)

        data = [input_data]

        column_names = ['Ausbaustufe', 'Baujahr', 'EG_qm', 'Gesamtqual', 'Gesamtzustand', 'Grundstueck_qm', 'Kellerhoehe', 'Steigung', 'Umgebaut', 'Verkaufsjahr', 'Wohnflaeche_qm',
                        'Besonderheiten_Familienverkauf', 'Besonderheiten_Pool', 'Lage_NeuBerlin_A', 'Lage_NeuBerlin_B', 'Lage_NeuBerlin_C']

        df_input = pd.DataFrame(data, columns=column_names)

        return df_input

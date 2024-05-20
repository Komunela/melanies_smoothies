# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
import pandas as pd
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie."""
)




my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name = title = st.text_input("Enter your name:")
st.write("Your name is:", title)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''

    for ingredient in ingredients_list:
        ingredients_string += ingredient + ', '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + ingredient)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)

    insert_stmt = """INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
                    VALUES('""" + ingredients_string + """', '""" + name + """')"""
    insert_button = st.button("Submit Order")

    if insert_button:
        session.sql(insert_stmt).collect()
        st.success("Your smoothie has been ordered. Thanks, " + name + "!", icon = "✅")
        


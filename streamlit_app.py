# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie."""
)

session = get_active_session()
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
    st.write(ingredients_string)

    insert_stmt = """INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
                    VALUES('""" + ingredients_string + """', '""" + name + """')"""
    insert_button = st.button("Submit Order")

    if insert_button:
        session.sql(insert_stmt).collect()
        st.success("Your smoothie has been ordered. Thanks, " + name + "!", icon = "✅")

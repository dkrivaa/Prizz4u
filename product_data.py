import streamlit as st


def all_product_data(product_code: str):
    """
    This function gets all data for the selected product
    :param product_code: Barcode for product
    :return:
    """
    # Getting price data
    price_data = [d for d in st.session_state['final_price'] if d['ItemCode'] == product_code][0]
    if price_data is None:
        price_data = [d for d in st.session_state['final_fullprice'] if d['ItemCode'] == product_code][0]

    item_data = [(d['ItemName'], d['ItemPrice']) for d in price_data]

    return item_data

import streamlit as st


def nav():
    """ This is the app navigation menu """
    with st.expander(label='Menu'):
        st.page_link(page='views/store.py')
        st.page_link(page='views/product.py')
        st.page_link(page='views/price.py')


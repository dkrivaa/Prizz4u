import streamlit as st


def nav():
    """ This is the app navigation menu """
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        with col1:
            st.page_link(page='views/store.py')
        with col2:
            st.page_link(page='views/product.py')
        with col3:
            st.page_link(page='views/price.py')


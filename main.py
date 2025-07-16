import os
os.system("playwright install")
import streamlit as st


st.set_page_config(
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header(':blue[Prizz4U]')
st.markdown('**Retail Price Transparency**')

st.divider()

store_page = st.Page(
    title='Store',
    page='views/store.py',
    default=True
)

product_page = st.Page(
    title='Product',
    page='views/product.py'
)

no_barcode_page = st.Page(
    title='No Barcode',
    page='views/no_barcode.py'
)

price_page = st.Page(
    title='Price',
    page='views/price.py'
)

pages = [store_page, product_page, price_page, no_barcode_page]


with st.container(border=True):
    col1, col2, col3, col4 = st.columns([1,1,1,2])
    with col1:
        st.page_link(page='views/store.py')
    with col2:
        st.page_link(page='views/product.py')
    with col3:
        st.page_link(page='views/price.py')

pg = st.navigation(pages=pages, position='hidden')
pg.run()

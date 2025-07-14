import streamlit as st


def display_price():
    """
    This is the function to display the product price
    """
    try:
        item_data = st.session_state['item_data']

        if len(item_data) > 0:
            st.metric(
                label=item_data[0],
                value=f'₪ {item_data[1]}'
            )

        else:
            st.metric(
                label='Product Price Is Not Available',
                value=None
            )

        st.divider()

        if st.button('Check Another Product'):
            st.switch_page('views/product.py')

    except KeyError:
        if 'store_list' not in st.session_state:
            st.switch_page('views/store.py')
        if 'price_list' not in st.session_state:
            st.switch_page('views/product.py')
        if 'item_data' not in st.session_state:
            st.switch_page('views/product.py')


if __name__ == "__main__":
    display_price()


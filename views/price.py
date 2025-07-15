import streamlit as st


def display_price():
    """
    This is the function to display the product price
    """
    try:
        with st.container(border=True):
            # PRICE
            item_price = st.session_state['item_price']

            st.write(st.session_state['store'])

            if len(item_price) > 0:
                st.metric(
                    label=item_price[0][0],
                    value=f'₪ {item_price[0][1]}'
                )

            else:
                st.metric(
                    label='Product Price Is Not Available',
                    value=None
                )

            st.divider()
            # SALES / DISCOUNTS
            st.markdown('**Sales / Discounts**')
            st.write(st.session_state['item_promo'])

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


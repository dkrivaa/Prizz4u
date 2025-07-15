import streamlit as st


def sales():
    """ This function presents the sales / discounts for selected product """

    item_promo = st.session_state['item_promo'][0]
    with st.container():
        st.metric(label=item_promo[0],
                  value=f'₪ {float(item_promo[2])}')
        if item_promo[1]:
            st.write(item_promo[1])
        if item_promo[3]:
            st.write(f'Minimum Quantity: {item_promo[3]}')
        if item_promo[4]:
            st.write(f'Maximum Quantity: {item_promo[4]}')
        if item_promo[5]:
            st.write(f'Minimal total Purchase: {item_promo[5]}')
        if item_promo[7]:
            value = int([d[0] for d in item_promo[7]][0])
            if value not in range(4):
                value=0
            with st.container(border=True):
                st.radio(
                    label='Limitations',
                    options=['No Limitation', 'Shufersal Club Members Only',
                             'Shufersal CreditCard Holders Only','Other', ],
                    index=value,
                    disabled=True
                )
        st.write(f'Sale/Discount Ends On: {item_promo[8]}')


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
            if len(st.session_state['item_promo']) > 0:
                # Display sale/discount
                sales()
            else:
                st.write('No Sales / Discounts')

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


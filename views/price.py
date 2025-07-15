import streamlit as st


def sales():
    """ This function presents the sales / discounts for selected product """

    item_promo = st.session_state['item_promo']
    st.write(item_promo['PromotionDescription'])
    # with st.container(border=True):
    #     description = item_promo['PromotionDescription']
    #     new_price = int(item_promo['DiscountedPrice'])
    #     st.metric(label=description,
    #               value=new_price)
    #     if item_promo('Remark'):
    #         st.write(item_promo['Remark'])
    #     if item_promo['MinQty']:
    #         st.write(f'Minimum Quantity: {item_promo['MinQty']}')
    #     if item_promo['MaxQty']:
    #         st.write(f'Maximum Quantity: {item_promo['MaxQty']}')
    #     if item_promo['MinAmount']:
    #         st.write(f'Minimal total Purchase: {item_promo['MinAmount']}')
    #     if item_promo['Clubs']:
    #         value = int([d[0] for d in item_promo['Clubs']][0])
    #         if value not in range(4):
    #             value=0
    #         st.radio(
    #             label='Audience',
    #             label_visibility='hidden',
    #             options=['No Limitation', 'Shufersal Club Members Only',
    #                      'Shufersal CreditCard Holders Only','Other', ],
    #             index=value,
    #             disabled=True
    #         )
    #     st.write(f'Sale/Discount Ends On: {item_promo['PromotionEndDate']}')


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


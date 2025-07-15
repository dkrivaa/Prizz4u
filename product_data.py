import streamlit as st


def all_product_data(product_code: str):
    """
    This function gets all data for the selected product
    :param product_code: Barcode for product
    :return:
    """
    # Getting price data
    price_data = [d for d in st.session_state['final_price'] if d['ItemCode'] == product_code]
    if not price_data:
        price_data = [d for d in st.session_state['final_fullprice'] if d['ItemCode'] == product_code]

    item_data = [(d['ItemName'], d['ItemPrice']) for d in price_data]

    # Getting promo data
    promo_data = [d for d in st.session_state['final_promo']
                  if any(f['ItemCode'] == product_code for f in d['PromotionItems'])]
    if not promo_data:
        promo_data = [d for d in st.session_state['final_fullpromo']
                      if (any(f['ItemCode'] == product_code for f in d['PromotionItems'])
                      and d['PromotionId'] not in ['242208', '4173926'])]

    item_promo = [
        (d.get('PromotionDescription'), d.get('Remark'), d.get('DiscountedPrice'),
         d.get('MinQty'), d.get('MaxQty'), d.get('MinAmount'), d.get('RewardType'),
         d.get('Clubs'), d.get('PromotionEndDate'), d.get('PromotionEndHour'))
        for d in promo_data]

    return item_data, item_promo



"""









"""
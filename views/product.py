import streamlit as st
import sys
import subprocess
import os

from PIL import Image
from pyzbar.pyzbar import decode as decode_pyzbar
import numpy as np
import cv2

from subprocess_results import make_final_price_data


def barcode():
    """
    This function enables user to upload pic of barcode and reads the code
    :return:
    """

    st.markdown("**Barcode Scanner**")

    uploaded_file = st.file_uploader("📸 Tap to upload or take a photo of barcode", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=False)

        # Convert to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Convert to grayscale
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

        # Slight contrast enhancement
        contrast = cv2.convertScaleAbs(gray, alpha=1.2, beta=20)

        # First try with pyzbar
        decoded_objects = decode_pyzbar(contrast)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')

        st.error("❌ No barcode or readable numeric code detected. Enter barcode manually.")
        return "No barcode or QR code detected."


@st.cache_data(ttl='2h', show_spinner=False)
def get_price_data(store_code):
    """ Getting price data for selected store """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    price_list_subprocess_result = subprocess.run(
        [sys.executable, 'async_prices.py', store_code],
        capture_output=True,
        text=True,  # automatically decodes output
        encoding='utf-8',  # 👈 force UTF-8 decoding
        env=env
    )

    return price_list_subprocess_result


def main():
    """
    This is the main function for the product page
    This page enables user to upload pic of barcode and reads the image_code
    """
    try:
        # Making price list for selected store
        with st.spinner('Getting data for Your store........'):
            # Using subprocess to get price data for selected store
            store_code = st.session_state['store_code']
            price_list_subprocess_result = get_price_data(store_code)
            # Transforming subprocess result to list of prices
            final_price_list = make_final_price_data(price_list_subprocess_result)
            st.session_state['price_list'] = final_price_list

        # Take barcode picture and get image_code
        with st.form('Submit Data', clear_on_submit=True):
            image_code = barcode()
            st.write(':blue[or]')
            st.markdown('**Enter Barcode**')
            write_code = st.text_input('Enter barcode')

            submitted = st.form_submit_button('Submit')

            if submitted:

                price_list = st.session_state['price_list']
                item_data = []

                # Priority: write_code (manual) > image_code (barcode scan)
                if write_code:
                    matching = [d for d in price_list if d['ItemCode'] == write_code]
                    if matching:
                        item_data = [matching[0]['ItemName'], matching[0]['ItemPrice']]
                elif image_code:
                    matching = [d for d in price_list if d['ItemCode'] == image_code]
                    if matching:
                        item_data = [matching[0]['ItemName'], matching[0]['ItemPrice']]

                st.divider()

                # Go to display item info
                if image_code or write_code:
                    if 'item_data' not in st.session_state:
                        st.session_state['item_data'] = item_data
                    else:
                        st.session_state['item_data'] = item_data

                    if image_code != 'No barcode or QR code detected.':
                        st.switch_page('views/price.py')

    except KeyError:
        if 'store_list' not in st.session_state:
            st.switch_page('views/store.py')
        if 'store_code' not in st.session_state:
            st.switch_page('views/store.py')


if __name__ == "__main__":
    main()


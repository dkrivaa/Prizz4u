import streamlit as st
import sys
import subprocess
import os
import re

from PIL import Image
from pyzbar.pyzbar import decode as decode_pyzbar
import numpy as np
import cv2

from subprocess_results import make_final_price_data, make_final_promo_data
from product_data import all_product_data


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
    """
    This function runs the subprocesses to get the data from the 4 price / promo files -
    price, fullprice, promo, fullpromo
    :param store_code: The code for selected store
    :return: a list of the data from the four files as strings of list of dicts
    """
    # Making sure store_code is string
    store_code = str(store_code)
    # Step 1: Run Crawl4AI to get the links
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    links_proc = subprocess.run(
        [sys.executable, "async_price_links.py", store_code],  # or your actual command
        capture_output=True,
        text=True,
        encoding='utf-8',  # 👈 force UTF-8 decoding
        env=env
    )

    # Step 2: Extract all URLs ending with `.gz`
    stdout = links_proc.stdout
    links = re.findall(r"https://[^\s]+?\.gz\?[^ \n]+", stdout)

    # Step 3: Validate and print
    if len(links) != 4:
        raise ValueError(f"Expected 4 URLs, got {len(links)}:\n{links}")

    # Optional: Assign clearly
    price_url, fullprice_url, promo_url, fullpromo_url = links

    # Show them
    for i, url in enumerate(links, 1):
        print(f"Link {i}: {url}")

    urls = [price_url, fullprice_url, promo_url, fullpromo_url]
    types = ['price', 'price', 'promo', 'promo']

    # Optional: Run each in a subprocess
    results = []
    for url, dtype in zip(urls, types):
        proc = subprocess.run(
            [sys.executable, "async_fetch_price_promo_data.py", url, dtype],
            capture_output=True,
            text=True,
            encoding='utf-8',  # 👈 force UTF-8 decoding
            env=env
        )
        results.append(proc.stdout)

    return results


def main():
    """
    This is the main function for the product page
    This page enables user to upload pic of barcode and reads the image_code
    """
    try:
        # Making price and promo lists for selected store
        with st.spinner('Getting data for Your store........'):
            # Using subprocess to get price data for selected store
            store_code = st.session_state['store_code']
            price_promo_lists_subprocess_result = get_price_data(store_code)

        # Making final lists for price and promo data
        final_price = make_final_price_data(price_promo_lists_subprocess_result[0])
        final_fullprice = make_final_price_data(price_promo_lists_subprocess_result[1])
        final_promo = make_final_promo_data(price_promo_lists_subprocess_result[2])
        final_fullpromo = make_final_promo_data(price_promo_lists_subprocess_result[3])

        st.write(final_promo[:10])

        def enter_into_session_state(name: str, data: list[dict[str, str]]):
            if name not in st.session_state:
                st.session_state[name] = data

        enter_into_session_state('final_price', final_price)
        enter_into_session_state('final_fullprice', final_fullprice)
        enter_into_session_state('final_promo', final_promo)
        enter_into_session_state('final_fullpromo', final_fullpromo)

        # Take barcode picture and get image_code
        with st.form('Submit Data', clear_on_submit=True):
            image_code = barcode()
            st.write(':blue[or]')
            st.markdown('**Enter Barcode**')
            write_code = st.text_input('Enter barcode')

            submitted = st.form_submit_button('Submit')

            if submitted:

                product_code = None

                if write_code:
                    product_code = write_code
                elif image_code and image_code != 'No barcode or QR code detected.':
                    product_code = image_code
                    # Get data for product

                item_price = []
                item_promo = []

                if product_code:
                    item_price, item_promo = all_product_data(product_code=product_code)
                    st.write(item_price)

                    if 'item_price' not in st.session_state:
                        st.session_state['item_price'] = item_price
                    else:
                        st.session_state['item_price'] = item_price

                    if 'item_promo' not in st.session_state:
                        st.session_state['item_promo'] = item_promo
                    else:
                        st.session_state['item_promo'] = item_promo

                    st.switch_page('views/price.py')

    except KeyError:
        if 'store_list' not in st.session_state:
            st.switch_page('views/store.py')
        if 'store_code' not in st.session_state:
            st.switch_page('views/store.py')


if __name__ == "__main__":
    main()


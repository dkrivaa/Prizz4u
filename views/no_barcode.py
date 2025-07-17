import streamlit as st

from navigator import nav


def main():
    """ This page is for when barcode on image is not recognized """
    # Add navigation menu to page
    nav()
    with st.container(border=True):
        st.subheader('❌ No barcode or QR code detected')
        st.markdown('Try again or **Enter barcode manually**')

        if st.button('Back'):
            st.switch_page('views/product.py')


if __name__ == "__main__":
    main()
import streamlit as st
import sys
import subprocess
import os

from subprocess_results import make_final_store_list


@st.cache_data(ttl='2h', show_spinner=False)
def get_store_data():
    """ Function to get store list"""

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    store_list_subprocess_result = subprocess.run(
        [sys.executable, 'async_stores.py', ],
        capture_output=True,
        text=True,  # automatically decodes output
        encoding='utf-8',  # 👈 force UTF-8 decoding
        env=env
    )

    return store_list_subprocess_result


def main():
    """
    This is the main function for the home page
    """

    # Making store list one time
    if 'store_list' not in st.session_state:
        with st.spinner('One Moment, Getting System Ready........'):
            # Using subprocess to get store data
            store_list_subprocess_result = get_store_data()
            # Transforming subprocess result to list of stores
            final_store_list = make_final_store_list(store_list_subprocess_result)
            st.session_state['store_list'] = final_store_list

    if 'store_list' in st.session_state:
        # Show store selectBox
        store = st.selectbox(
            label='Select Store',
            label_visibility='hidden',
            options=st.session_state['store_list'],
            index=None,
            placeholder='Select Store'
        )

        if store is not None:
            # Putting the store name in session_state
            if 'store' not in st.session_state:
                st.session_state['store'] = store
            store_code = store.split('-')[-1]

            if store_code:
                if 'store_code' not in st.session_state:
                    st.session_state['store_code'] = store_code
                else:
                    st.session_state['store_code'] = store_code

                if st.button('Go to Store'):
                    st.switch_page('views/product.py')


if __name__ == "__main__":
    main()

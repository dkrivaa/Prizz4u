import requests
import gzip
from io import BytesIO
import xml.etree.ElementTree as ET
from enum import Enum


class DataType(Enum):
    price = 1
    promo = 2
    stores = 3


async def extract_data_from_link(gz_url: str, data_type: DataType = DataType.price) -> list[dict[str, str]]:
    """
    This function transforms a download link to a list of dicts
    :param gz_url: download link
    :param price_data: bool True if price link
    :return: list of dicts of items in download link file
    """

    items = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://prices.shufersal.co.il",  # ⬅️ important if Azure checks referrer
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(gz_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.reason}")
        print(f"URL attempted: {gz_url}")
        raise

    # Decompress the GZIP file
    with gzip.GzipFile(fileobj=BytesIO(response.content)) as f:
        xml_data = f.read()

    # Parse XML from decompressed bytes
    root = ET.fromstring(xml_data)

    if data_type == DataType.price:
        # Extract all <Item> elements into list of dicts
        for item_elem in root.findall('.//Item'):
            item_data = {child.tag: child.text for child in item_elem}
            items.append(item_data)

    elif data_type == DataType.promo:
        # If the root is <asx:abap> → navigate down to <Promotion>
        promotions = root.findall('.//Promotion')

        for promo in promotions:
            promo_dict = {}

            # Extract direct child text fields
            for child in promo:
                if child.tag == 'PromotionItems':
                    promo_items = []
                    for item in child.findall('Item'):
                        item_dict = {elem.tag: elem.text for elem in item}
                        promo_items.append(item_dict)
                    promo_dict['PromotionItems'] = promo_items

                elif child.tag == 'AdditionalRestrictions':
                    restrictions = {elem.tag: elem.text for elem in child}
                    promo_dict['AdditionalRestrictions'] = restrictions

                elif child.tag == 'Clubs':
                    promo_dict['Clubs'] = [elem.text for elem in child.findall('ClubId')]

                else:
                    promo_dict[child.tag] = child.text

            items.append(promo_dict)

    else:
        # Extract namespaces
        ns = {'asx': 'http://www.sap.com/abapxml'}

        # Navigate to the STORES element
        stores = root.find('.//asx:values/STORES', namespaces=ns)
        if stores is not None:
            for store_elem in stores.findall('STORE'):
                store_data = {child.tag: child.text for child in store_elem}
                items.append(store_data)

    return items


async def make_store_list(store_data: list[dict[str, str]]):
    """
    This function returns a list of stores to be used as menu for user
    :param store_data - the extracted data from stores link
    """
    store_list = [
        tuple('' if x is None else x for x in (d['STORENAME'], d['CITY'], d['STOREID']))
        for d in store_data
    ]
    store_list = sorted(store_list, key=lambda x: int(x[-1]))
    return [' - '.join(item) for item in store_list]






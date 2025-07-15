from subprocess import CompletedProcess
import ast


def make_final_store_list(subprocess_result: CompletedProcess[str]):
    """
    This function transform the subprocess result into store list
    :param subprocess_result:
    """

    # Extract last line that contains the list of stores
    lines = subprocess_result.stdout.strip().splitlines()
    for line in reversed(lines):
        if line.startswith('[') and line.endswith(']'):
            try:
                stores_list = ast.literal_eval(line)
                break
            except Exception as e:
                print("Failed to parse list:", e)
                stores_list = []
                break
    else:
        stores_list = []

    # Result
    return stores_list


def make_final_price_data(list_string: str, ):
    """
    This function transform subprocess result into price list for selected store
    :param list_string: the data in file link
    """
    try:
        price_data = ast.literal_eval(list_string)

        # Ensure it's a list of dicts
        if isinstance(price_data, list) and all(isinstance(d, dict) for d in price_data):
            return price_data
        return []
    except Exception as e:
        print("Failed to extract price data:", e)
        return []


def make_final_promo_data(list_string: str):
    """
    This function transform subprocess result into promo list for selected store
    :param list_string: The data in file link
    """
    try:

        # Safely evaluate to Python list of dicts
        promotions = ast.literal_eval(list_string)

        # Confirm structure
        if isinstance(promotions, list) and all(isinstance(p, dict) for p in promotions):
            return promotions
        else:
            print("⚠️ Output is not a list of dicts.")
            return []

    except Exception as e:
        print(f"❌ Failed to extract promotion data: {e}")
        return []



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


def make_final_price_data(subprocess_result: CompletedProcess[str]):
    """
    This function transform subprocess result into price list for selected store
    :param subprocess_result:
    """
    try:
        # Get the last "[" which starts the price data
        last_list_index = subprocess_result.stdout.rfind("[{")
        if last_list_index == -1:
            return []

        raw_data_str = subprocess_result.stdout[last_list_index:]

        # Parse the string to a real Python object
        price_data = ast.literal_eval(raw_data_str)

        # Ensure it's a list of dicts
        if isinstance(price_data, list) and all(isinstance(d, dict) for d in price_data):
            return price_data
        return []
    except Exception as e:
        print("Failed to extract price data:", e)
        return []


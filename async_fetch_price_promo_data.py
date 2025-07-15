import asyncio
import sys

from extraction import extract_data_from_link, DataType


async def main():
    url = sys.argv[1]
    dtype = sys.argv[2]  # 'price' or 'promo'
    dtype = DataType.price if dtype == 'price' else DataType.promo
    data = await extract_data_from_link(url, data_type=dtype)
    print(data)


if __name__ == "__main__":
    asyncio.run(main())

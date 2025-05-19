import logging
from config import load_config
from util import *
from huffman import *
from test import *
from tabulate import tabulate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
BLOCK_SIZE = 16
from plot import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
config = load_config()

def main():
    data = file_to_bit_array(config["PDF_FILE"])
    if data != None:
        block_size = config["BLOCK_SIZE"]
        run_all_tests(data,block_size)


def test_different_file_types():
    FILE_NAMES = ["./books/kafka.txt", "./books/kafka.pdf", "./books/kafka.mobi", "./books/kafka.epub"]
    BLOCK_SIZE = 16
    for file_name in FILE_NAMES:
        data = read_file(file_name)
        original_bit_array = to_bit_array(data)

        compressed_data, codes, compressed_len, original_len = compress(original_bit_array, BLOCK_SIZE)
        compression_ratio = round(compressed_len / original_len * 10000) / 100

        table = [
            ["Original Length (bits)", original_len],
            ["Compressed Length (bits)", compressed_len],
            ["Compression Ratio (%)", compression_ratio],
        ]
        print(f"\nTesting file: {file_name}")
        print(tabulate(table, headers=["Metric", "Value"], tablefmt="grid"))

        decompressed_data = decode(compressed_data, codes)
        test(decompressed_data, original_bit_array, BLOCK_SIZE)


if __name__ == "__main__":
    main()

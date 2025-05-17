import logging
from config import load_config
from util import *
from huffman import *
from test import *
from plot import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    config = load_config()

    data = read_pdf(config["PDF_FILE"])
    if data == None:
        logging.warning("File not found.")
        return

    block_size = config["BLOCK_SIZE"]
    original_bit_array = to_bit_array(data)
    if not original_bit_array:
        logging.warning("File is empty. Nothing to compress.")
        return

    compressed_data, decompressed_data, compression_ratio, reduction_ratio = compress_and_decompress(
        original_bit_array, block_size)

    test(original_bit_array, decompressed_data, block_size)
    results = run_block_size_tests(original_bit_array)
    block_size_reduction_plot(results)
    

if __name__ == "__main__":
    main()

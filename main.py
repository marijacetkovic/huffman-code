import logging
from config import load_config
from huffman import *
from util import *
from test import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    config = load_config()
    data = read_pdf(config["PDF_FILE"])
    b_size = config["BLOCK_SIZE"]
    original_bit_array = to_bit_array(data)
    if not original_bit_array:
            logging.warning("Input data is empty.")
            return
    
    compressed_data, codes, compressed_len, original_len = measure_time(
        "Compression",
        compress,
        original_bit_array,
        b_size
    )
    
    logging.info(f"Original length: {original_len} bits")
    logging.info(f"Compressed length: {compressed_len} bits")
    logging.info(f"Compression ratio: {round(compressed_len/original_len*10000)/100}%")

    
    decompressed_data = measure_time(
        "Decompression",
        decode,
        compressed_data,
        codes
    )
    
    test(original_bit_array, decompressed_data, b_size)
    

if __name__ == "__main__":
    main()

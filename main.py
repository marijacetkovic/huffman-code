from config import load_config
from huffman import compress
from util import *


def main():
    config = load_config()
    data = read_pdf(config["PDF_FILE"])
    bit_array = to_bit_array(data)

    compressed_data, codes, compressed_len, original_len = compress(bit_array, config["BLOCK_SIZE"])
    # print(compressed_data, compressed_len, original_len)


if __name__ == "__main__":
    main()

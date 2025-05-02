from config import load_config
from huffman import compress
from util import *

def main():
    config = load_config()
    data = read_pdf(config["PDF_FILE"])
    bit_array = to_bit_array(to_byte_array(data))

    result = compress(bit_array, config["BLOCK_SIZE"])
    print(result)
    
if __name__ == "__main__":
    main()

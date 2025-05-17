import logging
from config import load_config
from util import *
from huffman import *
from test import *
from plot import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
config = load_config()

def main():
    data = file_to_bit_array(config["PDF_FILE"])
    if data != None: 
        block_size = config["BLOCK_SIZE"]
        run_all_tests(data,block_size)
    

if __name__ == "__main__":
    main()

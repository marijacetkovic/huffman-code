import logging
from main import config
from util import *
from huffman import compress_and_decompress
from plot import *

def run_all_tests(data: list[int], block_size: int):
    #basic test for default block size
    result = compress_and_decompress(data, block_size)
    equals(data, result["decompressed_data"], block_size)

    # test different block sizes and plot
    results = run_block_size_tests(data)
    block_size_reduction_plot(results)

    # test compr/decompr times across diff file sizes
    compression_times, decompression_times = test_time_by_file()
    print_time_table(compression_times, decompression_times)


def equals(original: list[int], decompressed: list[int], block_size: int) -> bool:
    padded_original = pad_bit_array(original, block_size)
    
    if decompressed == padded_original:
        logging.info("Decompressed data matches original.")
        return True
    else:
        logging.error("Decompressed data does not match original.")
        return False
    
def run_block_size_tests(data: list[int]):
    block_sizes = config["BLOCK_SIZES"]
    results = []

    for block_size in block_sizes:
        logging.info(f"Testing block size: {block_size}")
        result = compress_and_decompress(data, block_size)

        logging.info(f"Compression ratio: {result['compression_ratio']:.2f}%")
        logging.info(f"Reduction ratio: {result['reduction_ratio']:.2f}%")

        if equals(data, result["decompressed_data"], block_size):
            logging.info(f"Test passed for block size {block_size}\n")
            results.append((block_size, result["reduction_ratio"]))
        else:
            logging.error(f"Test failed for block size {block_size}\n")

    return results


def test_time_by_file(block_size: int = 16):
    FILES = config["TEST_FILES_SIZE"]
    compression_times = []
    decompression_times = []

    for name, path in FILES.items():
        print(f"Testing {name}...")
        data = file_to_bit_array(path)
        result = compress_and_decompress(data, block_size)
        compression_times.append((name, result["compression_time"]))
        decompression_times.append((name, result["decompression_time"]))

    return compression_times, decompression_times
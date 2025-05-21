import logging

from main import config
from util import file_to_bit_array, pad_bit_array
from huffman import compress_and_decompress
from plot import print_table, block_size_reduction_plot

def run_all_tests(data: list[int], block_size: int) -> None:
    logging.info("Starting all tests...")

    # Basic test for default block size
    logging.info(f"Running basic test with block size: {block_size}")
    result = compress_and_decompress(data, block_size)
    assert_equals(data, result["decompressed_data"], block_size)

    # Test for different file sizes
    #test_file_sizes()

    # Test for different file formats
    #test_file_formats()

    # Test for different block sizes
    #test_block_sizes()

    # test for different content entropy
    test_entropy()

    logging.info("All tests completed.")

def assert_equals(original: list[int], decompressed: list[int], block_size: int) -> bool:
    padded_original = pad_bit_array(original, block_size)
    if decompressed == padded_original:
        logging.info("Decompressed data matches original.")
        return True
    else:
        print("Decompressed data does not match original.")
        return False

def test_file_sizes() -> None:
    logging.info("Testing different file sizes...")
    files = config["TEST_FILE_SIZES"]
    results = run_compression_tests_for_files("File Size", files)
    print_table(
        "File Size",
        results["file_names"],
        results["compression_ratios"],
        results["reductions"],
        results["compression_times"],
        results["decompression_times"],
    )

def test_file_formats() -> None:
    logging.info("Testing different file formats...")
    files = config["TEST_FILE_FORMATS"]
    results = run_compression_tests_for_files("File Format", files)
    print_table(
        "File Format",
        results["file_names"],
        results["compression_ratios"],
        results["reductions"],
        results["compression_times"],
        results["decompression_times"],
    )

def test_block_sizes() -> None:
    logging.info("Testing different block sizes...")
    file_path = config["PDF_FILE"]
    block_sizes = config["TEST_BLOCK_SIZES"]

    compression_ratios: list[float] = []
    reductions: list[float] = []
    compression_times: list[float] = []
    decompression_times: list[float] = []
    block_sizes_to_reductions: list[tuple[int, float]] = []

    data = file_to_bit_array(file_path)

    for block_size in block_sizes:
        logging.info(f"Testing block size {block_size}...")
        result = compress_and_decompress(data, block_size)
        compression_ratios.append(result["compression_ratio"])
        reductions.append(result["reduction"])
        compression_times.append(result["compression_time"])
        decompression_times.append(result["decompression_time"])
        block_sizes_to_reductions.append((block_size, result["reduction"]))

    print_table(
        "Block Size",
        block_sizes,
        compression_ratios,
        reductions,
        compression_times,
        decompression_times,
    )

    block_size_reduction_plot(block_sizes_to_reductions)


def run_compression_tests_for_files(
        test_name: str, files: dict[str, str]
) -> dict[str, list[object]]:
    compression_ratios: list[float] = []
    reductions: list[float] = []
    compression_times: list[float] = []
    decompression_times: list[float] = []
    block_size = config["BLOCK_SIZE"]

    for name, path in files.items():
        logging.info(f"Testing {name} for {test_name}...")
        data = file_to_bit_array(path)
        result = compress_and_decompress(data, block_size)
        assert_equals(data, result["decompressed_data"], block_size)

        compression_ratios.append(result["compression_ratio"])
        reductions.append(result["reduction"])
        compression_times.append(result["compression_time"])
        decompression_times.append(result["decompression_time"])

    return {
        "file_names": list(files.keys()),
        "compression_ratios": compression_ratios,
        "reductions": reductions,
        "compression_times": compression_times,
        "decompression_times": decompression_times,
    }


def test_entropy() -> None:
    logging.info("Testing PDFs with different entropy levels...")

    files = config["TEST_ENTROPY"] 
    results = run_compression_tests_for_files("Different entropy", files)

    print_table(
        "Entropy Level",
        results["file_names"],
        results["compression_ratios"],
        results["reductions"],
        results["compression_times"],
        results["decompression_times"],
    )
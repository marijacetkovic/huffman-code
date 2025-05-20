import time
import logging

def read_file(path: str) -> bytearray | None:
    try:
        with open(path, "rb") as f:
            return bytearray(f.read())
    except:
        return None

# src:https://docs.python.org/3/library/string.html#formatspec
def byte_to_bit_array(arr: bytearray) -> list[int]:
    bit_array = []
    for byte in arr:
        bits = format(byte, '08b')
        bit_array.extend(int(b) for b in bits)
    return bit_array

def pad_bit_array(bit_array: list[int], b_size: int) -> list[int]:
    padding = (b_size - (len(bit_array) % b_size)) % b_size
    return bit_array + [0] * padding

def file_to_bit_array(file_path: str) -> list[int] | None:
    data = read_file(file_path)
    if data is None:
        logging.warning("File not found.")
        return None

    bit_array = byte_to_bit_array(data)
    if not bit_array:
        logging.warning("File is empty. Nothing to compress.")
        return None
    
    return bit_array

#src: https://realpython.com/python-timer/
def measure_time(label, func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    logging.info(f"{label} took {end - start:.6f} seconds")
    return result, end-start

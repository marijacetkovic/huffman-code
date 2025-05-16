import time
from main import logging

def read_pdf(path: str) -> bytearray:
    with open(path, "rb") as f:
        return bytearray(f.read())


# src: https://stackoverflow.com/questions/11624190/how-to-convert-string-to-byte-array-in-python
def to_byte_array(data: str) -> bytearray:
    encoded = data.encode('utf-8')
    array = bytearray(encoded)
    return array


# src:https://docs.python.org/3/library/string.html#formatspec
def to_bit_array(arr: bytearray) -> list[int]:
    bit_array = []
    for byte in arr:
        bits = format(byte, '08b')
        bit_array.extend(int(b) for b in bits)
    return bit_array

def pad_bit_array(bit_array: list[int], b_size: int) -> list[int]:
    padding = (b_size - (len(bit_array) % b_size)) % b_size
    return bit_array + [0] * padding

#src: https://realpython.com/python-timer/
def measure_time(label, func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    logging.info(f"{label} took {end - start:.6f} seconds")
    return result

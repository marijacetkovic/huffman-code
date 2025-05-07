from util import pad_bit_array
from main import logging

#basic test
def test(original: list[int], decompressed: list[int], block_size: int) -> bool:
    padded_original = pad_bit_array(original, block_size)
    
    if decompressed == padded_original:
        logging.info("Decompressed data matches original.")
        return True
    else:
        logging.error("Decompressed data does not match original.")
        return False
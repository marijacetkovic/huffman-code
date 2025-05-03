import pymupdf

#src: https://pymupdf.readthedocs.io/en/latest/recipes-text.html
def read_pdf(path: str) -> bytearray:
    with pymupdf.open(path) as doc:  
        text = "".join([page.get_text() for page in doc])
    return to_byte_array(text)

#src: https://stackoverflow.com/questions/11624190/how-to-convert-string-to-byte-array-in-python
def to_byte_array(data: str) -> bytearray:
    encoded = data.encode('utf-8')
    array = bytearray(encoded)
    return array

#src:https://docs.python.org/3/library/string.html#formatspec
def to_bit_array(arr: bytearray) -> list[int]:
    bit_array = []
    for byte in arr:
        bits = format(byte, '08b')
        bit_array.extend(int(b) for b in bits)
    return bit_array

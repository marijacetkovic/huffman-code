import pymupdf

#src: https://pymupdf.readthedocs.io/en/latest/recipes-text.html
def read_pdf(path):
    with pymupdf.open(path) as doc:  
        text = "".join([page.get_text() for page in doc])
    return text

#src: https://stackoverflow.com/questions/11624190/how-to-convert-string-to-byte-array-in-python
def to_byte_array(data):
    encoded = data.encode('utf-8')
    array = bytearray(encoded)
    return array

#src:https://docs.python.org/3/library/string.html#formatspec
def to_bit_array(arr):
    bit_array = []
    for byte in arr:
        bits = format(byte, '08b')
        bit_array.extend(bits)
    return bit_array
from config import load_config
from util import *

config = load_config()
data = read_pdf(config["PDF_FILE"])
byte_array = to_byte_array(data)
bit_array = to_bit_array(byte_array)
print(bit_array)



    
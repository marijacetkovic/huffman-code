import heapq
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Node:
    def __init__(self, symbol: tuple[int, ...] | None, freq: int):
        self.symbol = symbol
        self.freq = freq
        # children pointers
        self.left = None
        self.right = None

    # needed for heapq to sort frequencies
    def __lt__(self, other):
        return self.freq < other.freq

# builds min heap from frequency table
def build_heap(freq_table: dict[tuple[int, ...], int]) -> list[Node]:
    logging.info("Building heap from frequency table.")
    min_heap = []
    for sym, freq in freq_table.items():
        node = Node(sym, freq)
        heapq.heappush(min_heap, node)
    logging.info("Heap building complete.")
    return min_heap

def build_huffman(heap: list[Node]) -> Node:
    logging.info("Building Huffman tree.")
    # loop until only root left
    while len(heap) > 1:
        # get two blocks with smallest freq
        l_child = heapq.heappop(heap)
        r_child = heapq.heappop(heap)

        # create new internal node w sum of freq and no symbol
        node = Node(None, l_child.freq + r_child.freq)

        # connect to child nodes
        node.left = l_child
        node.right = r_child

        # push supersymbol back into heap
        heapq.heappush(heap, node)

    # no more symbols in heap return pointer to root
    logging.info("Huffman tree building complete.")
    return heap[0]

def generate_huffman_codes(root: Node) -> dict[tuple[int, ...], str]:
    logging.info("Generating Huffman codes.")
    codes = {}
    code = []
    stack = [(root, code)]

    while stack:
        node, code = stack.pop()

        # if leaf node assign code
        if node.symbol is not None:
            #using binary tuples as code
            codes[node.symbol] = tuple(code)

        # if internal node continue traversing the tree
        else:
            # add 0/1 to curr code and traverse from children
            if node.right:
                stack.append((node.right, code + [1]))
            if node.left:
                stack.append((node.left, code + [0]))

    logging.info("Huffman code generation complete.")
    return codes



def split_into_blocks(bit_array: list[int], b_size: int) -> list[tuple[int, ...]]:
    logging.info(f"Splitting bit array into blocks of size {b_size}.")
    # if cannot be split into perfect blocks pad
    if len(bit_array) % b_size != 0:
        padding = b_size - (len(bit_array) % b_size)
        # extend last block of data w zeros
        bit_array = bit_array + [0] * padding

    blocks = []
    # use b_size as step size for i
    for i in range(0, len(bit_array), b_size):
        # convert to tuple so it can be used as dict key for freq table
        blocks.append(tuple(bit_array[i:i + b_size]))

    logging.info(f"Splitting into blocks complete, {len(blocks)} blocks created.")
    return blocks

def build_frequency_table(blocks: list[tuple[int, ...]]) -> dict[tuple[int, ...], int]:
    logging.info("Building frequency table.")
    table = {}
    for block in blocks:
        table[block] = table.get(block, 0) + 1
    logging.info("Frequency table building complete.")
    return table

def compress(bit_array: list[int], block_size: int) -> dict[tuple[int, ...], str]:
    logging.info(f"Starting compression with block size {block_size}.")
    blocks = split_into_blocks(bit_array, block_size)
    freq_table = build_frequency_table(blocks)
    heap = build_heap(freq_table)
    tree = build_huffman(heap)
    codes = generate_huffman_codes(tree)

    # encode using codes
    res = encode(blocks, codes)

    logging.info("Compression complete.")
    return res, codes, len(res), len(bit_array)

def encode(blocks, codes):
    logging.info("Encoding blocks.")
    res = []
    for block in blocks:
        res.extend(codes[block])
    logging.info("Encoding complete.")
    return res

def decode(data):
    logging.info("Decoding data.")
    return data

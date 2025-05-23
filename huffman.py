import heapq
import logging
from util import pad_bit_array, measure_time
#src https://www.geeksforgeeks.org/huffman-coding-in-python/


class Node:
    def __init__(self, symbol: tuple[int, ...] | None, prob: int):
        self.symbol = symbol
        self.prob = prob
        # children pointers
        self.left = None
        self.right = None

    # needed for heapq to sort frequencies
    def __lt__(self, other):
        return self.prob < other.prob


# builds min heap from probability table
def build_heap(prob_table: dict[tuple[int, ...], float]) -> list[Node]:
    logging.info("Building heap from probability table.")
    min_heap = []
    for sym, prob in prob_table.items():
        node = Node(sym, prob)
        heapq.heappush(min_heap, node)
    logging.info("Heap building complete.")
    return min_heap

def build_huffman(heap: list[Node]) -> Node:
    logging.info("Building Huffman tree.")
    # loop until only root left
    while len(heap) > 1:
        # get two blocks with smallest prob
        l_child = heapq.heappop(heap)
        r_child = heapq.heappop(heap)

        # create new internal node w sum of freq and no symbol
        node = Node(None, l_child.prob + r_child.prob)

        # connect to child nodes
        node.left = l_child
        node.right = r_child

        # push supersymbol back into heap
        heapq.heappush(heap, node)

    # no more symbols in heap return pointer to root
    logging.info("Huffman tree building complete.")
    return heap[0]


def generate_huffman_codes(root: Node) -> dict[tuple[int, ...], tuple[int, ...]]:
    logging.info("Generating Huffman codes.")
    codes = {}
    code = []
    stack = [(root, code)]
    

    total_weighted_length = 0
    total_probability = 0

    # special case only one symbol in the data
    if root.symbol is not None:
        codes[root.symbol] = (0,)
        logging.info("Only one symbol in the tree. Assigned code 0. Average code length: 1.0")
        return codes
    
    while stack:
        node, code = stack.pop()

        # if leaf node assign code
        if node.symbol is not None:
            # using binary tuples as code
            codes[node.symbol] = tuple(code)
            total_weighted_length += len(code) * node.prob
            total_probability += node.prob

        # if internal node continue traversing the tree
        else:
            # add 0/1 to curr code and traverse from children
            if node.right:
                stack.append((node.right, code + [1]))
            if node.left:
                stack.append((node.left, code + [0]))

    logging.info(f"Huffman code generation complete, {len(codes)} codes created. Average code length: {total_weighted_length / total_probability:.4f}")
    return codes


def split_into_blocks(bit_array: list[int], b_size: int) -> list[tuple[int, ...]]:
    logging.info(f"Splitting bit array into blocks of size {b_size}.")
    # if cannot be split into perfect blocks pad
    bit_array = pad_bit_array(bit_array, b_size)

    blocks = []
    # use b_size as step size for i
    for i in range(0, len(bit_array), b_size):
        # convert to tuple so it can be used as dict key for freq table
        blocks.append(tuple(bit_array[i:i + b_size]))

    logging.info(f"Splitting into blocks complete, {len(blocks)} blocks created.")
    return blocks


def build_probability_table(blocks: list[tuple[int, ...]]) -> dict[tuple[int, ...], float]:
    logging.info("Building probability table.")
    # count raw frequencies
    freq_table = {}
    total_blocks = len(blocks)
    
    for block in blocks:
        freq_table[block] = freq_table.get(block, 0) + 1
    
    # convert to probabilities
    prob_table = {block: count/total_blocks 
                 for block, count in freq_table.items()}
    
    logging.info(f"Probability table building complete. Unique blocks: {len(prob_table)}")
    return prob_table

def compress(bit_array: list[int], block_size: int) -> tuple[
    list[int], dict[tuple[int, ...], tuple[int, ...]], int, int]:
    logging.info(f"Starting compression with block size {block_size}.")
    blocks = split_into_blocks(bit_array, block_size)
    prob_table = build_probability_table(blocks)
    heap = build_heap(prob_table)
    tree = build_huffman(heap)
    codes = generate_huffman_codes(tree)

    # encode using codes
    res = encode(blocks, codes)

    logging.info("Compression complete.")
    return res, codes, len(res), len(bit_array)


def encode(blocks: list[tuple[int, ...]], codes: dict[tuple[int, ...], tuple[int, ...]]) -> list[int]:
    logging.info("Encoding blocks.")
    res = []
    for block in blocks:
        res.extend(codes[block])
    logging.info("Encoding complete.")
    return res

def decode(encoded_bits: list[int], codes: dict[tuple[int, ...], tuple[int, ...]]) -> list[int]:
    logging.info("Decoding data.")
    
    # reverse the codes dictionary 
    reverse_codes = {v: k for k, v in codes.items()}
    decoded_bits = []
    current_code = []
    
    #loop over bits
    for bit in encoded_bits:
        current_code.append(bit)
        code_tuple = tuple(current_code)
        #if its a valid huffman code, get the original encoded block
        if code_tuple in reverse_codes:
            decoded_bits.extend(reverse_codes[code_tuple])

            #reset code
            current_code = []
    
    if current_code:
        logging.error("There are leftover bits.")
    logging.info("Decoding complete.")
    return decoded_bits

def compress_and_decompress(bit_array: list[int], block_size: int):
    (compressed_data, codes, compressed_len, original_len), compression_time = measure_time(
    "Compression", compress, bit_array, block_size
    )

    logging.info(f"Original length: {original_len} bits")
    logging.info(f"Compressed length: {compressed_len} bits")
    compression_ratio = original_len / compressed_len
    reduction = (1 - (compressed_len / original_len)) * 100.0

    logging.info(f"Compression ratio: {compression_ratio}")
    logging.info(f"Reduction: {reduction}%")


    decompressed_data, decompression_time = measure_time("Decompression", decode, compressed_data, codes)

    return {
            "compressed_data": compressed_data,
            "decompressed_data": decompressed_data,
            "compression_ratio": compression_ratio,
            "reduction": reduction,
            "compression_time": compression_time,
            "decompression_time": decompression_time,
    }
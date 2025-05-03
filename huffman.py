import heapq
#src https://www.geeksforgeeks.org/huffman-coding-in-python/

class Node:
    def __init__(self, symbol: tuple[int, ...] | None, freq: int):
        self.symbol = symbol
        self.freq = freq

        #children pointers
        self.left = None
        self.right = None

    #needed for heapq to sort frequencies
    def __lt__(self, other):
        return self.freq < other.freq

#builds min heap from frequency table 
def build_heap(freq_table: dict[tuple[int, ...], int]) -> list[Node]:
    min_heap = []
    for sym, freq in freq_table.items():
        node = Node(sym, freq)
        heapq.heappush(min_heap, node)
    return min_heap

def build_huffman(heap: list[Node]) -> Node:
    #loop until only root left
    while len(heap) > 1:
        #get two blocks with smallest freq
        l_child = heapq.heappop(heap)
        r_child = heapq.heappop(heap)

        #create new internal node w sum of freq and no symbol 
        node = Node(None, l_child.freq + r_child.freq)

        #connect to child nodes
        node.left = l_child
        node.right = r_child

        #push supersymbol back into heap
        heapq.heappush(heap, node)
    
    #no more symbols in heap return pointer to root
    return heap[0]

def generate_huffman_codes(root: Node) -> dict[tuple[int, ...], str]:
    codes = {}
    stack = [(root, "")] 
    
    while stack:
        node, code = stack.pop()
        
        #if leaf node assign code
        if node.symbol is not None:
            codes[node.symbol] = code

        #if internal node continue traversing the tree
        else:
            # add 0/1 to curr code and traverse from children
            if node.right:
                stack.append((node.right, code + "1"))
            if node.left:
                stack.append((node.left, code + "0"))
    
    return codes



def split_into_blocks(bit_array: list[int], b_size: int) -> list[tuple[int, ...]]:
    #if cannot be split into perfect blocks pad
    if len(bit_array) % b_size != 0:
        padding = b_size - (len(bit_array) % b_size)
        #extend last block of data w zeros
        bit_array = bit_array + [0] * padding
    
    blocks = []
    #use b_size as step size for i
    for i in range(0, len(bit_array), b_size):

        #convert to tuple so it can be used as dict key for freq table
        blocks.append(tuple(bit_array[i:i + b_size]))

    return blocks

def build_frequency_table(blocks: list[tuple[int, ...]]) -> dict[tuple[int, ...], int]:
    table = {}
    for block in blocks:
        table[block] = table.get(block, 0) + 1
    return table

def compress(bit_array: list[int], block_size: int) -> dict[tuple[int, ...], str]:
    blocks = split_into_blocks(bit_array, block_size)
    freq_table = build_frequency_table(blocks)
    heap = build_heap(freq_table)
    tree = build_huffman(heap)
    codes = generate_huffman_codes(tree)

    #encode using codes

    return codes

def decode(data):
    return data


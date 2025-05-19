import matplotlib.pyplot as plt
from tabulate import tabulate

#plot displaying file reduction percentage per diff block size
def block_size_reduction_plot(results: list[tuple[int, float]]):
    block_sizes = [x[0] for x in results]
    reduction_ratios = [x[1] for x in results]
    plt.plot(block_sizes, reduction_ratios)
    plt.grid(True)
    plt.xlabel("Block Size")
    plt.ylabel("Reduction (%)")
    plt.title("Reduction vs Block Size")
    plt.show()

#table displaying algorithm times for different file sizes
def print_time_table(compression_times, decompression_times):
    table_data = []
    for (name, c_time), (name, d_time) in zip(compression_times, decompression_times):
        table_data.append([name, round(c_time, 4), round(d_time, 4)])
    
    headers = ["File", "Compression Time (s)", "Decompression Time (s)"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


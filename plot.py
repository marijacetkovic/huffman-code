import matplotlib.pyplot as plt
from tabulate import tabulate

# plot displaying file reduction percentage per diff block size
def block_size_reduction_plot(results: list[tuple[int, float]]):
    block_sizes = [x[0] for x in results]
    reductions = [x[1] for x in results]
    plt.plot(block_sizes, reductions)
    plt.grid(True)
    plt.xlabel("Block Size")
    plt.ylabel("Reduction (%)")
    plt.title("Reduction vs Block Size")
    plt.show()

# table displaying algorithm times for different file sizes
def print_table(label, file_names, compression_ratios, reductions, compression_times, decompression_times):
    table_data = []
    for name, c_ratio, r_ratio, c_time, d_time in zip(file_names, compression_ratios, reductions, compression_times, decompression_times):
        table_data.append([name, round(c_ratio, 2), round(r_ratio, 2), round(c_time, 4), round(d_time, 4)])
    
    headers = [label, "Compression Ratio", "Reduction (%)", "Compression Time (s)", "Decompression Time (s)"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


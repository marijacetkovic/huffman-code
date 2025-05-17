import matplotlib.pyplot as plt

def block_size_reduction_plot(results: list[tuple[int, float]]):
    block_sizes = [x[0] for x in results]
    reduction_ratios = [x[1] for x in results]
    plt.plot(block_sizes, reduction_ratios)
    plt.grid(True)
    plt.xlabel("Block Size")
    plt.ylabel("Reduction (%)")
    plt.title("Reduction vs Block Size")
    plt.show()

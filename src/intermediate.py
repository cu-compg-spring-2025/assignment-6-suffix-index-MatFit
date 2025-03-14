import tracemalloc
import time
import suffix_array
import suffix_trie
import suffix_tree
import matplotlib.pyplot as plt
import argparse
import utils

def get_args():
    parser = argparse.ArgumentParser(description='Suffix Tree')

    parser.add_argument('--reference',
                        help='Reference sequence file',
                        type=str)

    parser.add_argument('--string',
                        help='Reference sequence',
                        type=str)

    parser.add_argument('--query',
                        help='Query sequences',
                        nargs='+',
                        type=str)

    return parser.parse_args()


def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]
    else:
        print("Error: No reference sequence provided")
        return

    trie_rt = []
    tree_rt = []
    array_rt = []

    trie_qrt = []
    tree_qrt = []
    array_qrt = []


    trie_bm = []
    tree_bm = []
    array_bm = []

    trie_qm = []
    tree_qm = []
    array_qm = []

    # Build test for size int(T / 2 * s)
    splits = 5
    x_values = []

    while splits > 0:
        length = len(T) // 2 * splits
        T_TEMP = T[:length]
        x_values.append(length)  # Store actual lengths for x-axis
        


        # Build Time and Memory for Trie
        start_time = time.time()
        tracemalloc.start()
        trie = suffix_trie.build_suffix_trie(T_TEMP)
        _, peak = tracemalloc.get_traced_memory()
        trie_bm.append(peak)
        tracemalloc.stop()
        end_time = time.time()
        trie_rt.append(end_time - start_time)

        # Build Time and Memory for Tree
        start_time = time.time()
        tracemalloc.start()
        tree = suffix_tree.build_suffix_tree(T_TEMP)
        _, peak = tracemalloc.get_traced_memory()
        tree_bm.append(peak)
        tracemalloc.stop()
        end_time = time.time()
        tree_rt.append(end_time - start_time)

        # Build Time and Memory for Array
        start_time = time.time()
        tracemalloc.start()
        array = suffix_array.build_suffix_array(T_TEMP)
        _, peak = tracemalloc.get_traced_memory()
        array_bm.append(peak)
        tracemalloc.stop()
        end_time = time.time()
        array_rt.append(end_time - start_time)



        # Query Memory
        if args.query:
            start_time = time.time()
            tracemalloc.start()
            for query in args.query:
                suffix_trie.search_trie(trie, query)
            _, peak = tracemalloc.get_traced_memory()
            trie_qm.append(peak)
            tracemalloc.stop()
            end_time = time.time()
            trie_qrt.append(end_time - start_time)
            
            start_time = time.time()
            tracemalloc.start()
            for query in args.query:
                suffix_tree.search_tree(tree, query)
            _, peak = tracemalloc.get_traced_memory()
            tree_qm.append(peak)
            tracemalloc.stop()
            end_time = time.time()
            tree_qrt.append(end_time - start_time)
            
            start_time = time.time()
            tracemalloc.start()
            for query in args.query:
                suffix_array.search_array(T_TEMP, array, query)
            _, peak = tracemalloc.get_traced_memory()
            array_qm.append(peak)
            tracemalloc.stop()
            end_time = time.time()
            array_qrt.append(end_time - start_time)
        else:
            trie_qm.append(0)
            tree_qm.append(0)
            array_qm.append(0)
            trie_qrt.append(0)
            tree_qrt.append(0)
            array_qrt.append(0)



        splits -= 1






    # Plot build runtime comparison
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, trie_rt, label='Suffix Trie', marker='o')
    plt.plot(x_values, tree_rt, label='Suffix Tree', marker='s')
    plt.plot(x_values, array_rt, label='Suffix Array', marker='^')
    plt.xlabel('Input Size (characters)')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime Comparison of Suffix Data Structures During Build')
    plt.legend()
    plt.grid(True)
    plt.savefig('../visuals/build_time_comparison.png')

    # Plot build memory comparison
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, trie_bm, label='Suffix Trie', marker='o')
    plt.plot(x_values, tree_bm, label='Suffix Tree', marker='s')
    plt.plot(x_values, array_bm, label='Suffix Array', marker='^')
    plt.xlabel('Input Size (characters)')
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Memory Usage Comparison of Suffix Data Structures During Build')
    plt.legend()
    plt.grid(True)
    plt.savefig('../visuals/build_memory_comparison.png')

    # Plot query memory comparison
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, trie_qm, label='Suffix Trie Query', marker='o')
    plt.plot(x_values, tree_qm, label='Suffix Tree Query', marker='s')
    plt.plot(x_values, array_qm, label='Suffix Array Query', marker='^')
    plt.xlabel('Input Size (characters)')
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Query Memory Usage Comparison of Suffix Data Structures')
    plt.legend()
    plt.grid(True)
    plt.savefig('../visuals/query_memory_comparison.png')


    plt.figure(figsize=(10, 6))
    plt.plot(x_values, trie_qrt, label='Suffix Trie Query', marker='o')
    plt.plot(x_values, tree_qrt, label='Suffix Tree Query', marker='s')
    plt.plot(x_values, array_qrt, label='Suffix Array Query', marker='^')
    plt.xlabel('Input Size (characters)')
    plt.ylabel('Runtime (seconds)')
    plt.title('Query Runtime Comparison of Suffix Data Structures')
    plt.legend()
    plt.grid(True)
    plt.savefig('../visuals/query_time_comparison.png')

if __name__ == '__main__':
    main()
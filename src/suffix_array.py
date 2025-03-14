import argparse
import utils
import suffix_tree

SUB = 0
CHILDREN = 1

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

def build_suffix_array(T):
    # Your code here
    tree = suffix_tree.build_suffix_tree(T)
    suffixes = []
    
    #defs
    # stack = [0]
    stack = [(0, "")] # Tuple of index and string
    while stack:
        node_idx, idx_string = stack.pop() # Pop from back

        node = tree[node_idx]
        substring = node[SUB]
        current_string = idx_string + substring

        if "$" in current_string:
            suffix = current_string.replace("$", "") # Safer than [:-1] because it will only remove "$" if it exists if not it wont do anything
            position = len(T) - len(suffix) # grab index position
            suffixes.append((position, suffix)) # Append string and it's index


        for _, child_index in tree[node_idx][CHILDREN].items(): # Just need the index
            stack.append((child_index, current_string))

    suffixes.sort(key=lambda x: x[1])
    suffix_array = [pos for pos, _ in suffixes]

    return suffix_array



# Overlap check
def overlap_length(s1, s2):
    min_len = min(len(s1), len(s2))
    for i in range(min_len):
        if s1[i] != s2[i]:
            return i
    return min_len

def search_array(T, suffix_array, q):

    # Your code here
    # ... 
    # binary search
    lo= 0
    hi = len(suffix_array) - 1
    max_overlap = 0


    while (lo <= hi):
        mid = int((lo + hi) / 2)
        suffix_split = T[suffix_array[mid]:]


        # Split and adjust depending on inequality
        if suffix_split < q:
            lo = mid + 1 # Look right
        elif suffix_split > q:
            hi = mid - 1 # Look left
        else:
            return len(suffix_split) # Perfect match 

        # Keep track of max overlap in case that a perfect match isn't found
        current_overlap = overlap_length(suffix_split, q)
        max_overlap = max(current_overlap, max_overlap)
        

    return max_overlap

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]
        
        
    print(T)
    array = build_suffix_array(T)


    if args.query:
        for query in args.query:
            match_len = search_array(T, array, query) # Will adjust to test time, was missing T parameter
            print(f'{query} : {match_len}')

if __name__ == '__main__':
    main()

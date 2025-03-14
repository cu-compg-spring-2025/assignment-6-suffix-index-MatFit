import argparse
import utils

def get_args():
    parser = argparse.ArgumentParser(description='Suffix Trie')

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

def build_suffix_trie(s):
    # YOUR CODE HERE
    trie = {}
    s = s + "$" # from : https://www.youtube.com/watch?v=VA9m_l6LpwI
    
    for i in range(len(s)):
        root = trie  # Current is a REFERENCE to trie, this also resets it to root
        for char in s[i:]:
            if char not in root:
                root[char] = {}  # Character : Dictionary
            root = root[char]  # Move to the next dictionary, e.g [Character : Dictionary1[Character : Dictionary2]]. Go from Dictionary1 -> Dictionary2
    
    return trie

def search_trie(trie, pattern):
    # YOUR CODE HERE
    current = trie
    overlap_len = 0
    
    for char in pattern:
        if char in current:
            overlap_len += 1
            current = current[char]
        else:
            break
    
    return overlap_len

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]


    print(T)
    trie = build_suffix_trie(T)
    
    
    if args.query:
        for query in args.query:
            match_len = search_trie(trie, query) # Will adjust to test time
            print(f'{query} : {match_len}')

if __name__ == '__main__':
    main()

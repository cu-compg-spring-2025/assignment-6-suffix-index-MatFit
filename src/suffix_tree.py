import argparse
import utils

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


def add_suffix(nodes, suf):
    n = 0
    i = 0
    while i < len(suf):
        b = suf[i] 
        children = nodes[n][CHILDREN]
        if b not in children:
            n2 = len(nodes)
            nodes.append([suf[i:], {}])
            nodes[n][CHILDREN][b] = n2
            return
        else:
            n2 = children[b]

        sub2 = nodes[n2][SUB]
        j = 0
        while j < len(sub2) and i + j < len(suf) and suf[i + j] == sub2[j]:
            j += 1

        if j < len(sub2):
            n3 = n2 
            n2 = len(nodes)
            nodes.append([sub2[:j], {sub2[j]: n3}])
            nodes[n3][SUB] = sub2[j:]
            nodes[n][CHILDREN][b] = n2

        i += j
        n = n2

def build_suffix_tree(text):
    text += "$"

    root = [ ['', {}] ]

    for i in range(len(text)):
        add_suffix(root, text[i:]) # adding suffix text[i:] into root
    
    return root

def search_tree(suffix_tree, P):
    # Your code here

    n = 0
    match_len = 0
    i = 0
    
    while i < len(P):
        if not suffix_tree[n][CHILDREN]:
            break
            
        char = P[i]
        
        if char not in suffix_tree[n][CHILDREN]:
            break
        
        child_node = suffix_tree[n][CHILDREN][char]
        substring = suffix_tree[child_node][SUB]
        
        j = 0
        while j < len(substring) and i + j < len(P) and P[i + j] == substring[j]:
            j += 1
        
        match_len += j
        i += j
        
        if j == len(substring):
            n = child_node
        else:
            break
    
    return match_len


def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]


    print(T)
    tree = build_suffix_tree(T)
    

    if args.query:
        for query in args.query:
            match_len = search_tree(tree, query) # Will adjust to test time
            print(f'{query} : {match_len}')

if __name__ == '__main__':
    main()

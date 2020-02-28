class HuffmanNode:
    def __init__(self, char_ascii, freq):
        self.char_ascii = char_ascii  # stored as an integer - the ASCII character code value
        self.freq = freq              # the frequency count associated with the node
        self.left = None              # Huffman tree (node) to the left
        self.right = None             # Huffman tree (node) to the right

    def __lt__(self, other):
        return comes_before(self, other) # Allows use of Python List sorting

    def __repr__(self):
        return "%s %s %s %s" % (self.char_ascii, self.freq, self.left, self.right)

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

def comes_before(a, b):
    """Returns True if node a comes before node b, False otherwise"""
    if a.freq < b.freq:
        return True
    elif a.freq == b.freq:
        if a.char_ascii < b.char_ascii:
            return True
    return False

def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    if a.char_ascii < b.char_ascii:
        ascii = a.char_ascii
    else:
        ascii = b.char_ascii

    newNode = HuffmanNode(ascii,(a.freq + b.freq))

    if comes_before(a, b) == True:
        newNode.set_left(a)
        newNode.set_right(b)
    else:
        newNode.set_left(b)
        newNode.set_right(a)

    return newNode

def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""
    entry_list = [0]*256

    with open(filename) as f:
        while True:
            c = f.read(1)
            if not c:
                break
            entry_list[ord(c)] += 1
    return entry_list


def create_huff_tree(freq_list):
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""
    if sum(freq_list) == 0:
        return None
    node_list = []
    for askii, frequency in enumerate(freq_list):
        if frequency != 0:
            new_node = HuffmanNode(askii, frequency)
            node_list.append(new_node)
    node_list = sorted(node_list)
    while(len(node_list) > 1):
        temp = []
        x = combine(node_list[0],node_list[1])
        temp.append(x)
        node_list = temp + node_list[2:]
        sorted(node_list)

    return node_list[0]

    #Attempt with a different method

    # if sum(freq_list) == 0:
    #     return None
    # node_list = []
    # break_flag = False
    # for askii, frequency in enumerate(freq_list):
    #     if frequency != 0:
    #         new_node = HuffmanNode(askii, frequency)
    #         if len(node_list) == 0:
    #             node_list.append(new_node)
    #         else:
    #             for index, node in enumerate(node_list):
    #                 if comes_before(new_node, node) == True:
    #                     node_list.insert(index, new_node)
    #                     break_flag = True
    #                     break
    # if break_flag == True:
    #     node_list.append(new_node)
    # print(node_list)
    # while (len(node_list) > 1):
    #     x = combine(node_list[0], node_list[1])
    #     node_list.pop(0)
    #     node_list.pop(0)
    #     for index, node in enumerate(node_list):
    #         if comes_before(x, node) == True:
    #             node_list.insert(index, x)
    #             break
    # return node_list[0]

def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""

    prefix_codes = [None] * 256

    def code_helper(node, prefix, inlist):
        if node.left == None and node.right == None:
            inlist[node.char_ascii] = prefix
        else:
            code_helper(node.left, prefix + "0", inlist)
            code_helper(node.right, prefix + "1", inlist)

    code_helper(node, "", prefix_codes)

    return prefix_codes


def create_header(freq_list):
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    final_list = ""

    for i in range(len(freq_list)): #number should be value and not index?
        # print(number)
        if freq_list[i] != 0:
            final_list += str(i)
            final_list += " "
            final_list += str(freq_list[i])
            final_list += " "
    final_list = final_list[:-1]

    return final_list


    #create a new list with [index, count, index, count...]
        #loop through the frequency list and append the index and value at that index
    #merge the new items of the list into a string (add space between each value in the list)


def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""

    freq_list = cnt_freq(in_file)
    tree = create_huff_tree(freq_list) #something is going wrong here or next line...
    code = create_code(tree)
    outf = open(out_file, "w")
    outf.write(create_header(freq_list))
    outf.write("\n")
    inf = open(in_file, "r")
    input = inf.read()
    for char in input:
        print(code[ord(char)] + " ")
        outf.write(code[ord(char)])
    outf.close()

def parse_header(header_string):
    entry_list = [0] * 256
    list1 = header_string.split()
    for index in range(0, len(list1), 2):
        freq_value = int(list1[index+1])
        entry_list[int(list1[index])] = freq_value
    return entry_list

def huffman_decode(encoded_file, decode_file):
    try:
        f = open(encoded_file, "r")
    except:
        raise FileNotFoundError
    d = open(decode_file, "w+")
    first_line = f.readline()
    freq_list = parse_header(first_line)
    tree = create_huff_tree(freq_list)
    second_line = f.readline()
    current = tree
    for number in second_line:
        if number == "0":
            current = current.left
            if current.left == None and current.right == None:
                d.write(chr(current.char_ascii))
                current = tree
        elif number == "1":
            current = current.right
            if current.left == None and current.right == None:
                d.write(chr(current.char_ascii))
                current = tree



# huffman_encode("file1.txt", "file1_binary.txt")
# huffman_decode("file1_soln.txt", "file1_letters.txt")
# print(parse_header("97 2 98 4 99 8 100 16 102 2"))








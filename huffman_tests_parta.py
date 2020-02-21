import unittest
from huffman import *

class TestList(unittest.TestCase):
#     def test_cnt_freq(self):
#         freqlist	= cnt_freq("file2.txt")
#         anslist = [2, 4, 8, 16, 0, 2, 0]
#         self.assertListEqual(freqlist[97:104], anslist)
#
#     def test_create_huff_tree(self):
#         freqlist = cnt_freq("file2.txt")
#         hufftree = create_huff_tree(freqlist)
#         self.assertEqual(hufftree.freq, 32)
#         self.assertEqual(hufftree.char_ascii, 97)
#         left = hufftree.left
#         self.assertEqual(left.freq, 16)
#         self.assertEqual(left.char_ascii, 97)
#         right = hufftree.right
#         self.assertEqual(right.freq, 16)
#         self.assertEqual(right.char_ascii, 100)
#
#     def test_create_header(self):
#         freqlist = cnt_freq("file2.txt")
#         self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")
#
#     def test_create_code(self):
#         freqlist = cnt_freq("file2.txt")
#         hufftree = create_huff_tree(freqlist)
#         codes = create_code(hufftree)
#         self.assertEqual(codes[ord('d')], '1')
#         self.assertEqual(codes[ord('a')], '0000')
#         self.assertEqual(codes[ord('f')], '0001')
#
#     def test_01_textfile(self):
#         huffman_encode("file1.txt", "file1_out.txt")
#         # capture errors by comparing your encoded file with a *known* solution file
#         self.assertTrue(compare_files("file1_out.txt", "file1_soln.txt"))

    def test_02_textfile(self):
        huffman_encode("test3.txt", "file3_out.txt")

# Compare files - takes care of CR/LF, LF issues
def compare_files(file1,file2):
    match = True
    done = False
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            while not done:
                line1 = f1.readline().strip()
                line2 = f2.readline().strip()
                if line1 == '' and line2 == '':
                    done = True
                if line1 != line2:
                    done = True
                    match = False
    return match

if __name__ == '__main__': 
   unittest.main()

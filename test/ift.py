import os
import sys
import unittest
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.

sys.path.append(parent)
 
# now we can import the module in the parent
# directory.

from interp import interpret

class InterpTest(unittest.TestCase):
    def test_ift(self):
        self.assertEqual(interpret("(if #t (if #t 1 2) 2)"),'1')

if __name__ == '__main__':
    unittest.main()
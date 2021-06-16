import unittest

'''
reference: https://docs.python.org/3/library/unittest.html
'''
'''
this template uses a module and a function we create in class to aid comprehension.
'''

# 1. get the function to test.
from myModule import getRevCompl

# 2. create a class into which we pass the unit tests we want to perform.
class myModuleTests(unittest.TestCase):

   # 3. create a method for each test to perform.
   def test_getRevCompl(self):
       result = getRevCompl("gattaca")
       # here, the test ensures that output of the function is indeed the expected output.
       self.assertEqual(result, "tgtaatc")

# 4. finally, we run the unit tests defined within the class.
# we can modify verbosity level (default=1) to get more or less info as tests run. 
unittest.main(verbosity=2)

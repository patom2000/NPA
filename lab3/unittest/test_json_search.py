import unittest
from recursive_json_search import *
from test_data import *
class json_search_found(unittest.TestCase):
    '''test module to test search function in `recursive_json_search.py`'''
    def test_search_found(self):
        '''key should be found, return list should not be empty'''
        print(1, json_search(key1, data))
        self.assertTrue([]!=json_search(key1, data))
    def test_search_not_found(self):
        '''key should not be found, should return an empty list'''
        print(2, json_search(key2, data))
        self.assertTrue([]==json_search(key2, data))
    def test_is_a_list(self):
        '''should return a list'''
        print(3, json_search(key1, data))
        self.assertIsInstance(json_search(key1, data), list)
if __name__ == '__main__':
    unittest.main()

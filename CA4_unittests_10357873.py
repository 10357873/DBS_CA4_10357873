#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 18:30:15 2017

@author: ciaran
"""

import unittest
from CA4_10357873 import count_lines_in_datafile
from CA4_10357873 import create_data_frame
changes_file = 'changes_python.txt'


class TestCommits(unittest.TestCase):
    
    #create variable which has count of lines in file
    def setUp(self):
        self.data = count_lines_in_datafile(changes_file)
        
    #test that the number of lines in the file matches 5255
    def test_number_of_lines(self):
        self.assertEqual(5255, (self.data))
        
    #test various items from the dataframe match what they should
    def test_number_of_commits(self):
        commits = create_data_frame(changes_file,self.data)
        self.assertEqual(422, len(commits))
        self.assertEqual('Thomas', commits.iloc[0]['user'])
        self.assertEqual('Jimmy', commits.iloc[420]['user'])
        self.assertEqual('FTRPC-500: Frontier Android || Inconsistencey in My Activity screen', commits.iloc[24]['comment'])
        self.assertEqual(259, commits.iloc[26]['added'])
        self.assertEqual('r1551249', commits.iloc[14]['commit block'])


if __name__ == '__main__':
    unittest.main()
import unittest
import os
import sys
import pandas as pd
import random

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import ProcessWordSnippets as Pws


class ProcessWordSnippetsTestss(unittest.TestCase):
    def setUp(self):
        self.image_tar_path = 'tests/resources/images.tar'
        self.json_tar_path = 'tests/resources/json.tar'
        self.snippets_tsv_path = 'tests/resources/classificationTsv'
        self.output_dir = 'tests/aaaTestResults'
        self.no_path = './not/a/valid_path'
        if os.path.exists(self.output_dir):
            raise Exception("If test results directory already exists, you must delete it manually to preform tests.\n" +
            "\tPlease now delete " + self.output_dir + " test restults directory.")

    def test_ProcessWordSnippets_success(self):
        # initialize correct values
        files = ['15thcensus872unit_1033', 'michigancensus00reel974_0221', 'newyorkcensus00reel1415rs_0920', 
                'michigancensus00reel974_0114']
        file_paths = ['tests/aaaTestResults/' + file_name for file_name in files]
        file_lengths = [9, 9, 10, 5]
        photos = [['15thcensus872unit_1033_row_0_col_3.jpg', '15thcensus872unit_1033_row_0_col_8.jpg',
                '15thcensus872unit_1033_row_0_col_9.jpg', '15thcensus872unit_1033_row_0_col_10.jpg', '15thcensus872unit_1033_row_2_col_3.jpg', 
                '15thcensus872unit_1033_row_2_col_4.jpg', '15thcensus872unit_1033_row_3_col_15.jpg', '15thcensus872unit_1033_row_4_col_26.jpg', 
                '15thcensus872unit_1033_row_5_col_16.jpg'],
                ['michigancensus00reel974_0221_row_0_col_3.jpg', 'michigancensus00reel974_0221_row_0_col_4.jpg', 
                'michigancensus00reel974_0221_row_0_col_6.jpg', 'michigancensus00reel974_0221_row_0_col_8.jpg', 
                'michigancensus00reel974_0221_row_0_col_9.jpg', 'michigancensus00reel974_0221_row_0_col_10.jpg', 
                'michigancensus00reel974_0221_row_0_col_11.jpg', 'michigancensus00reel974_0221_row_0_col_12.jpg', 
                'michigancensus00reel974_0221_row_0_col_13.jpg'],
                ['newyorkcensus00reel1415rs_0920_row_0_col_25.jpg', 'newyorkcensus00reel1415rs_0920_row_1_col_3.jpg', 
                'newyorkcensus00reel1415rs_0920_row_6_col_14.jpg', 'newyorkcensus00reel1415rs_0920_row_8_col_18.jpg', 
                'newyorkcensus00reel1415rs_0920_row_13_col_13.jpg', 'newyorkcensus00reel1415rs_0920_row_22_col_18.jpg', 
                'newyorkcensus00reel1415rs_0920_row_41_col_12.jpg', 'newyorkcensus00reel1415rs_0920_row_47_col_4.jpg', 
                'newyorkcensus00reel1415rs_0920_row_49_col_30.jpg', 'newyorkcensus00reel1415rs_0920_row_49_col_34.jpg'],
                ['michigancensus00reel974_0114_row_1_col_18.jpg', 'michigancensus00reel974_0114_row_3_col_13.jpg',
                'michigancensus00reel974_0114_row_6_col_3.jpg', 'michigancensus00reel974_0114_row_6_col_6.jpg',
                'michigancensus00reel974_0114_row_6_col_28.jpg']]
        
        # run code
        pws = Pws.ProcessWordSnippets()
        pws.process_word_snippets(self.snippets_tsv_path, self.image_tar_path, self.json_tar_path,
                                  self.output_dir)
        
        # perform tests
        self.assertEqual(files, os.listdir(self.output_dir))
        for i in range(len(file_paths)):
            self.assertEqual(file_lengths[i], len(os.listdir(file_paths[i])))
            for photo in photos[i]:
                self.assertIn(photo, os.listdir(file_paths[i]))
        
        # user verification
        tsv_paths = ['tests/resources/classificationTsv/' + file_name + '.tsv' for file_name in files]
        all_correct_words = []
        for tsv_file in tsv_paths:
            data = pd.read_csv(tsv_file, sep='\t', header=0)
            word_rows = data.loc[data['type'] == 'word']
            tsv_correct_words = list(zip(word_rows['row'], word_rows['column'], word_rows['content']))
            all_correct_words.append(tsv_correct_words)
        
        # test two random words from each folder
        print("\n\nUSER INPUT REQUIRED!!!\n")
        for i in range(len(all_correct_words)):
            test1 = random.randrange(len(all_correct_words[i]))
            test2 = random.randrange(len(all_correct_words[i]))
            if test1 == test2 and test2 > 1:
                test2 -= 1
            elif test1 == test2:
                test2 += 1

            jpg_name1 = files[i] + '_row_' + str(all_correct_words[i][test1][0]) + '_col_' + str(all_correct_words[i][test1][1]) + '.jpg'
            correct_word1 = all_correct_words[i][test1][2]
            jpg_name2 = files[i] + '_row_' + str(all_correct_words[i][test2][0]) + '_col_' + str(all_correct_words[i][test2][1]) + '.jpg'
            correct_word2 = all_correct_words[i][test2][2]
        
            answer1 = input("Does " + jpg_name1 + " say '" + correct_word1 + "'? (Y/n)")
            if answer1 == 'n':
                raise Exception(jpg_name1 + " is not correct.")
            answer2 = input("Does " + jpg_name2 + " say '" + correct_word2 + "'? (Y/n)")
            if answer2 == 'n':
                raise Exception(jpg_name2 + " is not correct.")
        
        print("\nThank you. Please now delete " + self.output_dir + " test restults directory.")


    def test_ProcessWordSnippets_badPaths(self):
        pws = Pws.ProcessWordSnippets()
        self.assertRaises(Exception, pws.process_word_snippets, self.no_path, self.no_path, self.no_path,
                          self.output_dir)

if __name__ == "__main__":
    unittest.main()
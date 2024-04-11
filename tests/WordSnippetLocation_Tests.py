import unittest
from .. import WordSnippetLocation as WSL


class TestWordLocationFunction(unittest.TestCase):
    def setUp(self):
        self.success1_file = 'RLL_Snippet_Generator/tests/resources/wordSnippetLocation_test1.tsv'
        self.success2_file = 'RLL_Snippet_Generator/tests/resources/wordSnippetLocation_test2.tsv'
        self.fail1_file = 'RLL_Snippet_Generator/tests/resources/wordSnippetLocation_fail1.tsv'
        self.no_file = './not_a_valid_file.tsv'
        # if not get_all_snippets:
            # if i,j not in desired_snippets

    def test_getWordLocations_success1(self):
        test1tsv_solution = {(4, 4), (3, 4), (4, 1), (3, 1), (1, 1), (1, 4), (2, 3), (2, 2), (3, 2), (1, 3)}
        self.assertEqual(WSL.get_word_locations_from_tsv(self.success1_file), test1tsv_solution)

    def test_getWordLocations_success2(self):
        test2tsv_solution = {(1, 1), (1, 2), (1, 3), (1, 4), (3, 1), (3, 2), (3, 4), (3, 5), (4, 1), (4, 2),
                             (4, 4), (4, 5), (5, 1), (5, 2), (5, 5), (6, 1), (6, 2), (6, 4), (6, 5)}
        self.assertEqual(WSL.get_word_locations_from_tsv(self.success2_file), test2tsv_solution)

    def test_getWordLocations_badTsvFormat(self):
        self.assertRaises(Exception, WSL.get_word_locations_from_tsv, self.fail1_file)

    def test_getWordLocations_noFile(self):
        self.assertRaises(Exception, WSL.get_word_locations_from_tsv, self.no_file)
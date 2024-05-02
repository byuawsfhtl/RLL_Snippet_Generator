import unittest
import glob
import os

def test_suite_from_recursive_discover(folder, pattern):
    """Provides test suite object containing tests found in the given folder that begin with the given pattern.

    Args:
        folder (str): path to the folder to search for tests
        pattern (str): regex to match the names of tests we would like to store in the suite

    Returns:
        TestSuite: a unittest object representing an aggregation of test cases
    """
    test_files = glob.glob(f'{folder}/**/{pattern}', recursive=True)
    test_dirs = list(set(([os.path.dirname(os.path.abspath(test_file)) for test_file in test_files])))

    suites = [unittest.TestLoader().discover(start_dir=d, pattern=pattern) for d in test_dirs]
    suite = unittest.TestSuite(suites)
    return suite
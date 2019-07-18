import unittest

from .test_ncread import test_classes as task_ncreads
#from .test_matplot import test_classes as task_matplots
#from .test_ncplot import test_classes as task_ncplots


def nctools_unittest_suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    #all_tests = task_netcdfs + task_matplots + task_ncplots
    all_tests = task_ncreads

    for test_class in all_tests:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    return suite

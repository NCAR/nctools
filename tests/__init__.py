import unittest

from .test_netcdf import test_classes as task_netcdfs
from .test_matplot import test_classes as task_matplots
from .test_ncplot import test_classes as task_ncplots


def nctools_unittest_suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    all_tests = task_ncplots + task_netcdfs + task_matplots

    for test_class in all_tests:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    return suite
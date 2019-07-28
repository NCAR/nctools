import unittest
from pyloco.test import TestSuite

from .test_ncread import test_classes as task_ncreads
from .test_ncdump import test_classes as task_ncdumps
from .test_nccalc import test_classes as task_nccalcs
from .test_ncplot import test_classes as task_ncplots


def nctools_unittest_suite():

    loader = unittest.TestLoader()
    suite = TestSuite()

    all_tests = task_ncreads + task_ncdumps + task_nccalcs + task_ncplots

    for test_class in all_tests:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    return suite

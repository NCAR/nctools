"""nctools nccalc test module
"""

from __future__ import unicode_literals

import os
import unittest

import nctools

here, myname = os.path.split(__file__)
datadir = os.path.join(here, "data")
rootdir = os.path.realpath(os.path.join(here, ".."))
datafile = os.path.join(datadir, "sresa1b_ncar_ccsm3-example.nc")

class TaskNcReadTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sum(self):

        argv = [datafile, "-c", "numpy.sum(pr[:])"]
        retval, forward = nctools.perform("nccalc", argv)

        self.assertEqual(retval, 0)
        self.assertIn("data", forward)
        self.assertIn("_", forward["data"])
        self.assertTrue(abs(forward["data"]["_"] - 0.8931981921195984) < 1.0E-15)


    def test_slicesum(self):

        argv = [datafile, "-c", "x=numpy.sum(pr[0,:,0])"]
        retval, forward = nctools.perform("nccalc", argv)

        self.assertEqual(retval, 0)
        self.assertIn("data", forward)
        self.assertIn("x", forward["data"])
        self.assertTrue(abs(forward["data"]["x"] - 0.0034066441003233) < 1.0E-15)


test_classes = (TaskNcReadTests,)

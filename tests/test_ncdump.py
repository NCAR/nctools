"""nctools ncread test module
"""

from __future__ import unicode_literals

import os
import unittest

import nctools
import numpy

here, myname = os.path.split(__file__)
datadir = os.path.join(here, "data")
rootdir = os.path.realpath(os.path.join(here, ".."))
datafile = os.path.join(datadir, "sresa1b_ncar_ccsm3-example.nc")
testppf= os.path.join(datadir, "test.ppf")

class TaskNcReadTests(unittest.TestCase):

    def setUp(self):
        if os.path.exists(testppf):
            os.remove(testppf)

    def tearDown(self):
        if os.path.exists(testppf):
            os.remove(testppf)

    def test_dumpall(self):

        argv = [datafile, "-q"]
        retval, forward = nctools.perform("ncdump", argv)

        self.assertEqual(retval, 0)
        self.assertIn("data", forward)
        self.assertEqual(forward["data"], None)

    def test_var(self):

        argv = [datafile, "-p", "pr", "-q"]
        retval, forward = nctools.perform("ncdump", argv)

        self.assertEqual(retval, 0)
        self.assertIn("data", forward)
        self.assertIn("data", forward["data"])
        self.assertTrue(isinstance(forward["data"]["data"], (numpy.ndarray, numpy.generic)))

    def test_var_attr(self):

        argv = [datafile, "-p", "pr.shape", "-q"]
        retval, forward = nctools.perform("ncdump", argv)

        self.assertEqual(retval, 0)
        self.assertIn("data", forward)
        self.assertEqual(forward["data"], (1, 128, 256))

    def test_dim_attr(self):

        argv = [datafile, "-p", "lat.size", "-q"]
        retval, forward = nctools.perform("ncdump", argv)

        self.assertEqual(retval, 0)
        self.assertIn("data", forward)
        self.assertEqual(forward["data"], 128)
        

    def test_attr(self):

        argv = [datafile, "-p", "model_name_english", "-q"]
        retval, forward = nctools.perform("ncdump", argv)

        self.assertEqual(retval, 0)
        self.assertIn("data", forward)
        self.assertEqual(forward["data"], "NCAR CCSM")

test_classes = (TaskNcReadTests,)

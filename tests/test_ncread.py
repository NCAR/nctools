"""nctools ncread test module
"""

from __future__ import unicode_literals

import os
import unittest

import nctools

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

    def test_read(self):

        argv = ["ncread", datafile, "-p", "pr", "--write-pickle", testppf, "-q"]

        retval = nctools.main(argv)

        self.assertEqual(retval, 0)
        self.assertTrue(os.path.exists(testppf))


    def test_pickle(self):


        argv = ["ncread", datafile, "--write-pickle", testppf, "-p", "pr", "-q"]

        retval = nctools.main(argv)

        self.assertEqual(retval, 0)
        self.assertTrue(os.path.exists(testppf))

        argv = ["input", "--read-pickle", testppf, "--assert-input", "'dims' in data[0]"]
        retval = nctools.main(argv)

        self.assertEqual(retval, 0)


test_classes = (TaskNcReadTests,)

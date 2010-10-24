# Copyright 2010 The Untemplate Authors.  All Rights Reserved.

"""Tests for 'untemplate'."""

import untemplate

import unittest



class GDataUtilityTest(unittest.TestCase):
  """Test case for GData utility methods."""

  def testGetData(self):
    self.assertEquals(
      ('World', 'Earth'),
      untemplate.getData(
        'Hello World!',
        'Hello Earth!'
      )
    )

# Copyright 2010 The Untemplate Authors.  All Rights Reserved.

"""Tests for 'untemplate'."""

import untemplate

import unittest



class GDataUtilityTest(unittest.TestCase):
  """Test case for GData utility methods."""

  def testGetData(self):
    # Test the basic case.
    self.assertEquals(
      [['World'], ['Earth']],
      untemplate.getData(
        'Hello World!',
        'Hello Earth!'
      )
    )

    # Test a case where the template defined by the first two documents isn't generic enough.
    self.assertEquals(
      [['Mary Kate'], ['Mary Jane'], ['Bob']],
      untemplate.getData(
        'Hello Mary Kate.  How are you?',
        'Hello Mary Jane.  How are you?',
        'Hello Bob.  How are you?'
      )
    )

    # No matter which two documents we try first, the template will not be generic enough.  Also tests
    # multiple simultaneous return values.
    self.assertEquals(
      [['1', '2', '3'], ['2', '2', '4'], ['1', '7', '8']],
      untemplate.getData(
        '1 + 2 = 3',
        '2 + 2 = 4',
        '1 + 7 = 8'
      )
    )


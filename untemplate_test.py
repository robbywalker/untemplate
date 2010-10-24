# Copyright 2010 The Untemplate Authors.  All Rights Reserved.

"""Tests for 'untemplate'."""

import untemplate

import unittest



class UntemplateTest(unittest.TestCase):
  """Test case for untemplate methods."""

  def testCompareLists(self):
    self.assertEquals(
      (1, ['=', 'S']),
      untemplate.compareLists(
        ['Hello', 'World'],
        ['Hello', 'Earth'],
      )
    )

    self.assertEquals(
      (1, ['=', 'I', '=']),
      untemplate.compareLists(
        ['Hello', 'World'],
        ['Hello', 'Beautiful', 'World'],
      )
    )

    self.assertEquals(
      (2, ['=', 'S', 'I']),
      untemplate.compareLists(
        ['Hello', 'World'],
        ['Hello', 'Beautiful', 'Earth'],
      )
    )


  def testGetData(self):
    # Test the basic case.
    self.assertEquals(
      [[['World']], [['Earth']]],
      untemplate.getData(
        'Hello World',
        'Hello Earth'
      )
    )

    # Test a case where the template defined by the first two documents isn't generic enough.
    self.assertEquals(
      [[['Mary', 'Kate']], [['Mary', 'Jane']], [['Bob']]],
      untemplate.getData(
        'Hello Mary Kate How are you',
        'Hello Mary Jane How are you',
        'Hello Bob How are you'
      )
    )

    # Test another case where the template defined by the first two documents isn't generic enough.
    self.assertEquals(
      [[['Anne', 'Margaret']], [['Mary', 'Margaret']], [['Bob']]],
      untemplate.getData(
        'Hello Anne Margaret How are you',
        'Hello Mary Margaret How are you',
        'Hello Bob How are you'
      )
    )

    # Test another case where the template defined by the first two documents isn't generic enough.
    self.assertEquals(
      [[['B', 'C']], [['E']], [['E', 'C', 'D']]],
      untemplate.getData(
        'A B C D Z',
        'A E D Z',
        'A E C D D Z'
      )
    )

    # No matter which two documents we try first, the template will not be generic enough.  Also tests
    # multiple simultaneous return values.
    self.assertEquals(
      [[['1'], ['2'], ['3']], [['2'], ['2'], ['4']], [['1'], ['7'], ['8']]],
      untemplate.getData(
        '1 + 2 + 3 = 6',
        '1 + 3 + 5 = 9'
        '0 + 2 + 5 = 7'
      )
    )


#from tests import MyTest
import os
import sys
import unittest


def run():
    os.environ['MESSAGE_PARSER_CONFIG'] = 'testing'

    tests = unittest.TestLoader().discover('.')
    #ok = unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()
    ok = unittest.TextTestRunner().run(tests).wasSuccessful()
    sys.exit(0 if ok else 1)

    """
	mytest = MyTest()
	mytest.setUp()
	mytest.client_get()
	"""

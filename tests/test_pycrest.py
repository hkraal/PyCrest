'''
Created on Jun 27, 2016

@author: henk
'''
import os
import sys
from pycrest.eve import EVE, DictCache, APICache, FileCache
import httmock
import pycrest
import mock

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestApi(unittest.TestCase):

    def setUp(self):
        self.api = EVE()

    def test_endpoint_default(self):
        self.assertEqual(self.api._endpoint, 'https://crest-tq.eveonline.com/')
        self.assertEqual(self.api._image_server, 'https://image.eveonline.com/')
        self.assertEqual(self.api._oauth_endpoint, 'https://login.eveonline.com/oauth')

    def test_endpoint_testing(self):
        api = EVE(testing=True)
        self.assertEqual(api._endpoint, 'https://api-sisi.testeveonline.com/')
        self.assertEqual(api._image_server, 'https://image.testeveonline.com/')
        self.assertEqual(api._oauth_endpoint, 'https://sisilogin.testeveonline.com/oauth')


class TestAPIConnection(unittest.TestCase):

    def setUp(self):
        self.api = EVE()

    def test_user_agent(self):
        @httmock.all_requests
        def default_user_agent(url, request):
            user_agent = request.headers.get('User-Agent', None)
            self.assertEqual(user_agent, 'PyCrest/{0} +https://github.com/pycrest/PyCrest'.format(pycrest.version))

        with httmock.HTTMock(default_user_agent):
            eve = EVE()

        @httmock.all_requests
        def customer_user_agent(url, request):
            user_agent = request.headers.get('User-Agent', None)
            self.assertEqual(user_agent, 'PyCrest-Testing/{0} +https://github.com/pycrest/PyCrest'.format(pycrest.version))

        with httmock.HTTMock(customer_user_agent):
            eve = EVE(user_agent='PyCrest-Testing/{0} +https://github.com/pycrest/PyCrest'.format(pycrest.version))

    def test_headers(self):

        # Check default header
        @httmock.all_requests
        def check_default_headers(url, request):
            self.assertNotIn('PyCrest-Testing', request.headers)

        with httmock.HTTMock(check_default_headers):
            eve = EVE()
            eve()

        # Check custom header
        def check_custom_headers(url, request):
            self.assertIn('PyCrest-Testing', request.headers)

        with httmock.HTTMock(check_custom_headers):
            eve = EVE(additional_headers={'PyCrest-Testing': True})
            eve()

    def test_default_cache(self):
        self.assertTrue(isinstance(self.api.cache, DictCache))

    def test_callable_cache(self):
        class CustomCache(object):
            pass
        eve = EVE(cache=CustomCache)
        self.assertTrue(isinstance(eve.cache, CustomCache))

    def test_apicache(self):
        eve = EVE(cache=DictCache())
        self.assertTrue(isinstance(eve.cache, DictCache))

    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('os.mkdir')
    def test_cache_dir(self, mkdir_function, isdir_function):
        eve = EVE(cache_dir=TestFileCache.DIR)
        self.assertEqual(eve.cache_dir, TestFileCache.DIR)
        self.assertTrue(isinstance(eve.cache, FileCache))


class TestAPICache(unittest.TestCase):

    def setUp(self):
        self.c = APICache()

    def test_put(self):
        self.assertRaises(NotImplementedError, self.c.get, 'key')

    def test_get(self):
        self.assertRaises(NotImplementedError, self.c.put, 'key', 'val')

    def test_invalidate(self):
        self.assertRaises(NotImplementedError, self.c.invalidate, 'key')


class TestDictCache(unittest.TestCase):

    def setUp(self):
        self.c = DictCache()
        self.c.put('key', True)

    def test_put(self):
        self.assertEqual(self.c._dict['key'], True)

    def test_get(self):
        self.assertEqual(self.c.get('key'), True)

    def test_invalidate(self):
        self.c.invalidate('key')
        self.assertIsNone(self.c.get('key'))

    def test_cache_dir(self):
        pass


class TestFileCache(unittest.TestCase):
    '''
    Class for testing the filecache

    TODO: Debug wth this test is creating an SSL connection
    '''

    DIR = '/tmp/TestFileCache'

    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    def setUp(self, mkdir_function, isdir_function):
        self.c = FileCache(TestFileCache.DIR)

    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('os.mkdir')
    def test_init(self, mkdir_function, isdir_function):
        c = FileCache(TestFileCache.DIR)

        # Ensure path has been set
        self.assertEqual(c.path, TestFileCache.DIR)

        # Ensure we checked if the dir was already there
        args, kwargs = isdir_function.call_args
        self.assertEqual((TestFileCache.DIR,), args)

        # Ensure we called mkdir with the right args
        args, kwargs = mkdir_function.call_args
        self.assertEqual((TestFileCache.DIR, 0o700), args)

#     @unittest.skip("https://github.com/pycrest/PyCrest/issues/4")
#     def test_getpath(self):
#         self.assertEqual(self.c._getpath('key'), os.path.join(TestFileCache.DIR, '1140801208126482496.cache'))

if __name__ == "__main__":
    unittest.main()

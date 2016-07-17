'''
Created on Jul 17, 2016

@author: henk
'''
from pycrest.eve import EVE, FileCache
import unittest


class TestSingularity(unittest.TestCase):

    def setUp(self):
        self.api = EVE(client_id="00e75119c2c94a7184d1e123b5be91c0",
                       api_key="VOCgb6GHoDYzOn9h1LyAzD5eHn1zs6GOibGTlRYJ",
                       redirect_uri="http://localhost:8000/",
                       cache=FileCache('/tmp'))

    def test_root(self):
        root = self.api()
        self.assertTrue(hasattr(root, 'systems'))
        self.assertTrue(hasattr(root, 'marketTypes'))

    def test_systems(self):
        root = self.api().systems()
        jita = [x for x in root.items if x.name == 'Jita'][0]
        self.assertEqual(jita.name, 'Jita')

    def test_markettypes(self):
        root = self.api().marketTypes()
        tritanium = [x for x in root.items if x.type.name == 'Tritanium'][0]
        self.assertEqual(tritanium.id, 34)

    def test_auth(self):
        print(self.api.auth_uri(scopes=['publicData', 'characterLocationRead'], state="foobar"))
        auth = self.api.authorize(code='LsJTJK6RrFtzO4sfWlTaBGTEF8whquzPXrMG77ebVOLMKm75oYwrhscUs27cvwgh0')
#         print(auth().__dict__)
        print(auth.whoami())
#         print(auth.get('https://crest-tq.eveonline.com/characters/530529272/location'))


if __name__ == "__main__":
    unittest.main()

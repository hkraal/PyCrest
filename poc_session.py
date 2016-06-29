'''
Created on Jun 29, 2016

@author: henk
'''
import requests
import mock
import httmock

class MyClass(object):
    
    def __init__(self, url):
        self._session = requests.Session()
        self._url = url
    
    def __call__(self):
        return self._session.get(self._url)

if __name__ == '__main__':
    @httmock.all_requests
    def google_mock(url, request):
        print(url)
        print(request)
        return 'Feeling lucky, punk?'

    api = MyClass('https://www.google.nl/')
    with httmock.HTTMock(google_mock):
        print(api().content)

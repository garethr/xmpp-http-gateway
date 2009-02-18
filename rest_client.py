from django.test import Client
from urllib import urlencode
from django.test.client import MULTIPART_CONTENT, BOUNDARY, encode_multipart
from StringIO import StringIO

class RestClient(Client):
    "Django's test client doesn't do put/delete etc - but this one does"
    # Derived from patch on http://code.djangoproject.com/ticket/5888
    def head(self, path, data={}, **extra):
        "Request a response from the server using HEAD."
        r = {
            'CONTENT_LENGTH':  None,
            'CONTENT_TYPE':    'text/html; charset=utf-8',
            'PATH_INFO':       path,
            'QUERY_STRING':    urlencode(data, doseq=True),
            'REQUEST_METHOD': 'HEAD',
        }
        r.update(extra)
        
        return self.request(**r)
    
    def options(self, path, data={}, **extra):
        "Request a response from the server using OPTIONS."
        r = {
            'CONTENT_LENGTH':  None,
            'CONTENT_TYPE':    None,
            'PATH_INFO':       path,
            'QUERY_STRING':    urlencode(data, doseq=True),
            'REQUEST_METHOD': 'OPTIONS',
        }
        r.update(extra)
        
        return self.request(**r)
    
    def put(self, path, data={}, content_type=MULTIPART_CONTENT, **extra):
        "Send a resource to the server using PUT."
        if content_type is MULTIPART_CONTENT:
            post_data = encode_multipart(BOUNDARY, data)
        else:
            post_data = data

        r = {
            'CONTENT_LENGTH': len(post_data),
            'CONTENT_TYPE':   content_type,
            'PATH_INFO':      path,
            'REQUEST_METHOD': 'PUT',
            'wsgi.input':     StringIO(post_data),
        }
        r.update(extra)
        
        return self.request(**r)
        
    def delete(self, path, **extra):
        "Send a DELETE request to the server."
        r = {
            'PATH_INFO':      path,
            'REQUEST_METHOD': 'DELETE',
            'CONTENT_LENGTH':  None,
            'CONTENT_TYPE':    None,
            'PATH_INFO':       path,
            'REQUEST_METHOD': 'DELETE',
        }
        r.update(extra)
        
        return self.request(**r)
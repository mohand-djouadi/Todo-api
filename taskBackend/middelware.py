import logging
from django.utils.deprecation import MiddlewareMixin

class LogRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger = logging.getLogger('django')
        logger.info('Request Method: %s', request.method)
        logger.info('Request Headers: %s', request.headers)
        logger.info('CSRF Token (Cookie): %s', request.COOKIES.get('csrftoken'))
        logger.info('CSRF Token (Header): %s', request.META.get('HTTP_X_CSRFTOKEN'))
        return None

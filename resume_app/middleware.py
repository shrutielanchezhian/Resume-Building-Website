class SetContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'Content-Type' in response and 'charset' not in response['Content-Type']:
            response['Content-Type'] += '; charset=utf-8'
        return response

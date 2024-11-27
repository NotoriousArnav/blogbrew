# middleware.py
from user_agents import parse

class DeviceDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = parse(request.META['HTTP_USER_AGENT'])
        if user_agent.is_mobile:
            print("Mobile")
            request.is_mobile = True
        elif user_agent.is_tablet:
            request.is_tablet = True
        else:
            request.is_desktop = True

        response = self.get_response(request)
        return response



from django.http import HttpResponse

class CORSAllowOriginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/api/'):
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        return response

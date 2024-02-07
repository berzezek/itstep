from .models import Bb, Rubric


def simple_middleware(next):
    def core_middleware(request):
        print("before")
        response = next(request)
        print("after")
        return response

    return core_middleware


class RubricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_template_response(self, request, response):
        response.context_data["rubrics"] = Rubric.objects.all()
        return response


from django.contrib.auth.models import User


def rubrics(request):
    return {"rubrics": Rubric.objects.all()}

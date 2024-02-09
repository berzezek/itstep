from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Bb, Rubric
from django.views.generic.edit import CreateView
from .forms import BbForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect


class BbCreateView(CreateView):
    template_name = "bboard/create.html"
    form_class = BbForm
    success_url = reverse_lazy("index")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context


def index(request):
    bbs = Bb.objects.order_by("-published")
    # rubrics = Rubric.objects.all()
    context = {"bbs": bbs}
    # response = render(request, "bboard/index.html", context)
    # print(type(response))
    return TemplateResponse(request, "bboard/index.html", context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {"bbs": bbs, "rubrics": rubrics, "current_rubric": current_rubric}
    return render(request, "bboard/by_rubric.html", context)


def test_cookies(request):
    if "counter" in request.COOKIES:
        cnt = int(request.get_signed_cookie("counter", salt="cookie")) + 1
    else:
        cnt = 1
    response = render(
        request,
        "bboard/test.html",
        {"title": "Sessions", "counter": cnt},
    )
    response.set_signed_cookie("counter", cnt, salt="cookie")
    return response


def test_session(request):
    # request.session.set_expiry(None)
    if "counter" in request.session:
        cnt = request.session["counter"] + 1
    else:
        cnt = 1
    request.session["counter"] = cnt
    print(dir(request.session.cycle_key()))
    return render(request, "bboard/test.html", {"title": "Sessions", "counter": cnt})


def test_1(request):
    request.session['foo'] = 'bar'
    return HttpResponse('Set foo=bar')

def test_2(request):
    return HttpResponse(request.session.get('foo', 'No foo'))
from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Bb, Rubric
from django.views.generic.edit import CreateView
from .forms import BbForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string


MESSAGE_LEVEL = messages.DEBUG

CRITICAL = 50


class BbCreateView(SuccessMessageMixin, CreateView):
    template_name = "bboard/create.html"
    form_class = BbForm
    success_url = reverse_lazy("index")
    success_message = "%(rubric)s was created successfully"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context
    
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            rubric=self.object.get_rubric(),
        )


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
    # request.session["foo"] = "bar"
    messages.add_message(request, CRITICAL, "A serious error occurred.")
    return redirect("index")
    # return HttpResponse("Set foo=bar")


def test_2(request):
    return HttpResponse(request.session.get("foo", "No foo"))


def test_message(request):
    messages.add_message(request, messages.SUCCESS, "Hello, world!")
    return redirect("index")


def test_send_console_email(request):
    # con = get_connection()
    # con.open()
    # context = {"user": request.user.username}
    # s = render_to_string("email/letter.txt", context)
    # em = EmailMessage(subject='Test', body=s, to=[request.user.email], from_email='wknduz@gmail.com', connection=con)
    # em.send()
    # con.close()
    em = EmailMultiAlternatives(subject='Test', body='Hello, world!', to=[request.user.email],)
    em.attach_alternative('<h1>Hello, world!</h1>', 'text/html')
    em.send()
    return HttpResponse("Email sent")

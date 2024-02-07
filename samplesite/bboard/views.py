from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Bb, Rubric
from django.views.generic.edit import CreateView
from .forms import BbForm
from django.urls import reverse_lazy


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

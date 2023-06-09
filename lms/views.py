import lms.models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class CoursePage(TemplateView):
    def get(self, request, **kwargs):
        all_course = lms.models.Course.objects.order_by("CreatedDate")
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('../../')

        context = {
            'Course': all_course,
        }

        return render(request, 'course_page.html', context)


def course_view(request, cat, slug):

    context = {
        'course': lms.models.Course.objects.filter(slug=slug).get(),
    }
    return render(request, 'course_single.html', context)

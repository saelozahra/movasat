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
        'lessons': lms.models.Lesson.objects.filter(Course__slug=slug).all(),
    }
    return render(request, 'course_single.html', context)


def lesson_view(request, cat, slug, lid):

    course = lms.models.Course.objects.filter(slug=slug).get()
    lms.models.Lesson.objects.filter(id=lid).update(view_count=int(course.view_count+1))

    context = {
        'course': course,
        'lessons': lms.models.Lesson.objects.filter(Course__slug=slug).all(),
    }

    return render(request, 'course_single.html', context)
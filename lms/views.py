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

    course = lms.models.Course.objects.filter(slug=slug)
    course.update(view_count=int(course.get().view_count+1))

    context = {
        'course': course.get(),
        'lessons': lms.models.Lesson.objects.filter(Course__slug=slug).all(),
        'edit_url': course.get().get_edit_url(),
    }
    return render(request, 'course_single.html', context)


def lesson_view(request, cat, slug, lid):

    course = lms.models.Course.objects.filter(slug=slug)
    course.update(view_count=int(course.get().view_count+1))

    this_lesson = lms.models.Lesson.objects.filter(id=lid)
    this_lesson.update(view_count=int(this_lesson.get().view_count)+1)

    context = {
        'course': course.get(),
        'this_lesson': this_lesson.all(),
        'lessons': lms.models.Lesson.objects.filter(Course__slug=slug).all(),
    }

    return render(request, 'course_single.html', context)

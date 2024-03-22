import account.models
import lms.models
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse


# Create your views here.


class CoursePage(TemplateView):
    def get(self, request, **kwargs):
        all_course = lms.models.Course.objects.order_by("CreatedDate")
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('../../')

        context = {
            'course': all_course,
        }

        return render(request, 'course_page.html', context)


def course_view(request, cat, slug):
    course = lms.models.Course.objects.filter(slug=slug)
    course.update(view_count=int(course.get().view_count + 1))

    context = {
        'registered': reg_in_this_course(request.user.id, course.get().id),
        'course': course.get(),
        'lessons': lms.models.Lesson.objects.filter(Course__slug=slug).all(),
        'edit_url': course.get().get_edit_url(),
    }
    return render(request, 'course_single.html', context)


def lesson_view(request, cat, slug, lid: int):
    course = lms.models.Course.objects.filter(slug=slug)
    course.update(view_count=int(course.get().view_count + 1))

    this_lesson = lms.models.Lesson.objects.filter(id=lid)
    this_lesson.update(view_count=int(this_lesson.get().view_count) + 1)

    context = {
        'registered': reg_in_this_course(request.user.id, course.get().id),
        'course': course.get(),
        'this_lesson': this_lesson.get(),
        'lessons': lms.models.Lesson.objects.filter(Course__slug=slug).all(),
        'next_lesson': lms.models.Lesson.objects.filter(Course__slug=slug, id__gt=lid).order_by('id').first(),
        'previous_lesson': lms.models.Lesson.objects.filter(Course__slug=slug, id__lt=lid).order_by('-id').first(),
        'edit_url': this_lesson.get().get_edit_url(),
    }

    return render(request, 'lesson_single.html', context)


def course_register(request, uid: int, cid: int):
    course = lms.models.Course.objects.get(id=cid)
    uid = int(uid)
    cid = int(cid)

    red_url = redirect("CourseView", cat=course.category, slug=course.slug)

    if request.user.id != uid:
        red_url['Location'] += '?res=bilakh'
        return red_url

    if not uid and not cid:
        red_url['Location'] += '?res=enter_cid'
        return red_url

    if reg_in_this_course(uid, cid):
        red_url['Location'] += '?res=reg_before'
        return red_url

    lms.models.CourseRegister.objects.create(
        user_id=uid,
        course_id=cid,
    )

    red_url['Location'] += '?res=success'

    return red_url


def reg_in_this_course(uid: int, coid: int):
    if uid and coid:
        urc = lms.models.CourseRegister.objects.filter(Student_id=uid, Course_id=coid)
    else:
        return False
    return urc.exists()

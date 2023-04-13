import lms.models
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class CoursePage(TemplateView):
    def get(self, request, **kwargs):
        # chat_id = kwargs.get("chat_id")
        all_course = lms.models.Course.objects.order_by("CreatedDate")

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('../../')

        context = {
            'Cource': all_course,
        }

        return render(request, 'course.html', context)

    # def post(self, request, **kwargs):
    #     chat_id = kwargs.get("chat_id")
    #     print("chat_id: " + chat_id)
    #     text = request.POST["text"]
    #     print("text: " + text)
    #
    #     try:
    #
    #         chm = ChatMessage()
    #         chm.Text = text
    #         chm.Tarikh = datetime.now()
    #         chm.RelatedChat = Chat.objects.filter(Q(id=chat_id)).get()
    #         chm.Sender = self.request.user
    #         chm.save()
    #         return HttpResponse("saved", status.HTTP_200_OK)
    #
    #     except NameError:
    #         print(NameError)
    #         return HttpResponse(NameError, status=status.HTTP_400_BAD_REQUEST)


def lesson_view(request, slug):

    context = {
        'ct_data': lms.models.Lesson.objects.filter(Q(slug__contains=slug)).get(),
    }
    return render(request, 'lesson.html', context)

from django.shortcuts import render, HttpResponseRedirect
from .models import Feedback
from donors.models import Donor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FeedbackForm


def feedback_list_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseRedirect('/')

    feedback_list = Feedback.objects.all()
    paginator = Paginator(feedback_list, 10)
    page = request.GET.get('page')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        feedbacks = paginator.page(1)
    except EmptyPage:
        feedbacks = paginator.page(paginator.num_pages)

    template = 'feedback.html'
    contex = {'feedbacks': feedbacks}
    return render(request, template, contex)



def feedback_create_view(request):
    template = 'feedback-create.html'
    form = FeedbackForm(request.POST or None, auto_id=False)
    msg = request.GET.get('msg', None)
    contex = {'form': form, 'msg': msg}
    if request.method == "POST":
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect("/feedback/create/?msg=success")
    return render(request, template, contex)


def feedback_detail_view(request, pk):
    if not request.user.is_superuser: return HttpResponseRedirect('/catalog/')
    template = 'feedback-detail.html'
    try:
        f = Feedback.objects.get(pk=pk)
    except:
        f = None
    return render(request, template, {'feedback': f})
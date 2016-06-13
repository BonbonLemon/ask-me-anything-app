from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
import pdb

from .models import AMA, Question, Answer


def index(request):
    latest_ama_list = AMA.objects.order_by('-pub_date')[:5]
    context = { 'latest_ama_list': latest_ama_list, }
    return render(request, 'index.html', context, context_instance=RequestContext(request))

def detail(request, ama_id):
    ama = get_object_or_404(AMA, pk=ama_id)
    return render(request, 'detail.html', {'ama': ama}, context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'email': request.POST.get('username', '')}, context_instance=RequestContext(request))
    else:
        return render(request, 'login.html', context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    print request.user
    return HttpResponseRedirect('/')

def signup(request):
    # pdb.set_trace()
    return render(request, 'signup.html', context_instance=RequestContext(request))
    # if request.method == 'POST':
    #     return render(request, 'signup.html')

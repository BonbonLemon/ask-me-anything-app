from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from models import AMA

from .models import AMA, Question, Answer

# Viewing
def index(request):
    latest_ama_list = AMA.objects.order_by('-pub_date')[:5]
    context = { 'latest_ama_list': latest_ama_list, }
    return render(request, 'index.html', context, context_instance=RequestContext(request))

def detail(request, ama_id):
    ama = get_object_or_404(AMA, pk=ama_id)
    return render(request, 'detail.html', {'ama': ama}, context_instance=RequestContext(request))

# Accounts
def login(request):
    next_path = ''
    if request.GET:
        next_path = request.GET['next']

    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if next_path:
                return HttpResponseRedirect(next_path)
            else:
                return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'username': username, 'errors': ['Invalid username or password'], 'next': next_path}, context_instance=RequestContext(request))
    else:
        context = {}
        if next_path:
            context['next'] = next_path
        return render(request, 'login.html', context, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        form = UserCreationForm({
            'username': username,
            'password1': password,
            'password2': password
        })
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'signup.html', {'errors': form.errors.values() }, context_instance=RequestContext(request))
    else:
        return render(request, 'signup.html', context_instance=RequestContext(request))

# Creation
@login_required
def createama(request):
    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title')
        # import pdb; pdb.set_trace()
        description_text = request.POST.get('description')
        ama = AMA(author=author, title=title, description_text=description_text)
        try:
            ama.clean()
        except ValidationError as errors:
            return render(request, 'create_ama.html', {'errors': errors}, context_instance=RequestContext(request))
        else:
            ama.save()
            return HttpResponseRedirect('/')
    else:
        return render(request, 'create_ama.html', context_instance=RequestContext(request))

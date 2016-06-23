from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from .models import AMA, Comment, Question, Answer

# Viewing
def index(request):
    latest_ama_list = AMA.objects.order_by('-pub_date')[:5]
    context = { 'latest_ama_list': latest_ama_list, }
    return render(request, 'ama/index.html', context, context_instance=RequestContext(request))

def detail(request, ama_id):
    ama = get_object_or_404(AMA, pk=ama_id)
    return render(request, 'ama/detail.html', {'ama': ama }, context_instance=RequestContext(request))

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
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'account/login.html', {'username': username, 'errors': ['Invalid username or password'], 'next': next_path}, context_instance=RequestContext(request))
    else:
        context = {}
        if next_path:
            context['next'] = next_path
        return render(request, 'account/login.html', context, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))

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
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'account/signup.html', {'errors': form.errors.values() }, context_instance=RequestContext(request))
    else:
        return render(request, 'account/signup.html', context_instance=RequestContext(request))

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
            return render(request, 'ama/create_ama.html', {'errors': errors}, context_instance=RequestContext(request))
        else:
            ama.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'ama/create_ama.html', context_instance=RequestContext(request))

def ask_question(request, ama_id):
    if request.method == 'POST':
        author = None
        if request.user.is_authenticated():
            author = request.user
        author_name = request.POST.get('author_name')
        if author_name == 'other':
            author_name = request.POST.get('other')
        ama = AMA.objects.get(id=int(ama_id))
        question_text = request.POST.get('question')
        new_question = Question(author_name=author_name, ama=ama, question_text=question_text)
        new_question.save()
        return HttpResponseRedirect(reverse('ama_detail', args=(int(ama_id),)))
    else:
        return HttpResponseRedirect(reverse('ama_detail', args=(int(ama_id),)))

@login_required
def question(request, ama_id, question_id):
    ama = get_object_or_404(AMA, pk=ama_id)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        # create answer/comment
        author = request.user
        if author == ama.author:
            if hasattr(question, 'answer'):
                question = get_object_or_404(Question, pk=question_id)
                answer = question.answer
                answer.answer_text = request.POST.get('response')
            else:
                question = Question.objects.get(id=int(question_id))
                answer_text = request.POST.get('response')
                answer = Answer(author=author, question=question, answer_text=answer_text)
            answer.save()
        else:
            comment_text = request.POST.get('response')
            comment = Comment(author=author, comment_text=comment_text, target=question)
            comment.save()
        # return render(request, 'ama/detail.html', {'ama': ama }, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('ama_detail', args=(int(ama.id),)))
        # return HttpResponse('OK')
        # return render(request, 'ama/question/detail.html', {'flash': "Response saved!", 'question': question, 'ama': ama}, context_instance=RequestContext(request))
    else:
        return render(request, 'ama/question/detail.html', {'question': question, 'ama': ama}, context_instance=RequestContext(request))

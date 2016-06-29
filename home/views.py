from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import TemplateView, View
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import AMA, Comment, Question, Answer
from .forms import UserForm

# Viewing
class AMAListView(ListView):
    template_name = 'ama/index.html'
    model = AMA
    paginate_by = 3

    def get_queryset(self):
        ordered_list = AMA.objects.order_by('-pub_date')
        return ordered_list

    def get_context_data(self, **kwargs):
        context = super(AMAListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context

class AMADetailView(DetailView):
    template_name = 'ama/detail.html'
    model = AMA

# Accounts
class UserFormView(View):
    form_class = UserForm
    template_name = 'account/signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')

        return render(request, self.template_name, {'form': form}, context_instance=RequestContext(request))

class SessionFormView(View):
    form_class = AuthenticationForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request):
        form = self.form_class(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
        return render(request, self.template_name, {'form': form}, context_instance=RequestContext(request))

class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

def vlogin(request):
    next_path = ''
    if request.GET:
        next_path = request.GET['next']

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
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

# Creation
# class AMACreateView(CreateView):
#     model = AMA
#     template_name = "ama/create_ama.html"
#     fields = ['title', 'description_text']

@login_required
def createama(request):
    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title')
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

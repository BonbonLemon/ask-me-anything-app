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
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .mixins import AuthRequiredMixin
from .models import AMA, Comment, Question, Answer
from .forms import UserForm, AMAForm, QuestionForm
# from .serializers import QuestionSerializer

# Viewing
class AMAListView(ListView):
    template_name = 'ama/index.html'
    model = AMA
    paginate_by = 10

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

class SessionFormView(FormView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm
    success_url = 'index'

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.GET:
            self.success_url = self.request.GET['next']
        return redirect(self.success_url)
    #
    # def get(self, request):
    #     form = self.form_class(None)
    #     return render(request, self.template_name, {'form': form}, context_instance=RequestContext(request))
    #
    # def post(self, request):
    #     form = self.form_class(request, request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         user = authenticate(username=username, password=password)
    #
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 next_path = 'index'
    #                 if request.GET:
    #                     next_path = request.GET['next']
    #                 return redirect(next_path)
    #     return render(request, self.template_name, {'form': form}, context_instance=RequestContext(request))

class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

# Creation
class AMACreateView(AuthRequiredMixin, CreateView):
    model = AMA
    template_name = "ama/create_ama.html"
    form_class = AMAForm

    def get_form(self):
        form = super(AMACreateView, self).get_form(self.form_class)
        form.instance.author = self.request.user
        return form

# class QuestionList(AuthRequiredMixin, APIView):
#
#     def get(self, request, format=None):
#         questions = Question.objects.all()
#         serializers = QuestionSerializer(questions, many=True)
#         return Response(serializers.data)
#
#     def post(self, request, format=None):
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class QuestionCreateView(AuthRequiredMixin, CreateView):
#     model = Question
#     form_class = QuestionForm
#
#     def get_form(self, form_class):
#         form = super(QuestionCreateView, self).get_form(form_class)
#         form.instance.author = self.request.user
#         import pdb; pdb.set_trace()
#         if self.request.author_name == 'other':
#             author_name = request.POST.get('other')
#         else:
#             author_name = self.request.user.username


def ask_question(request, ama_id):
    if request.method == 'POST':
        author = None
        if request.user.is_authenticated():
            author = request.user
        author_name = request.POST.get('author_name')
        if author_name == 'other':
            author_name = request.POST.get('other')
        ama = AMA.objects.get(id=int(ama_id))
        question = request.POST.get('question')
        new_question = Question(author_name=author_name, ama=ama, question=question)
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
                answer.answer = request.POST.get('response')
            else:
                question = Question.objects.get(id=int(question_id))
                answer = request.POST.get('response')
                answer = Answer(author=author, question=question, answer=answer)
            answer.save()
        else:
            comment = request.POST.get('response')
            comment = Comment(author=author, comment=comment, target=question)
            comment.save()
        # return render(request, 'ama/detail.html', {'ama': ama }, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('ama_detail', args=(int(ama.id),)))
        # return HttpResponse('OK')
        # return render(request, 'ama/question/detail.html', {'flash': "Response saved!", 'question': question, 'ama': ama}, context_instance=RequestContext(request))
    else:
        return render(request, 'ama/question/detail.html', {'question': question, 'ama': ama}, context_instance=RequestContext(request))

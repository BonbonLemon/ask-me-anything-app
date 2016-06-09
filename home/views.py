from django.http import HttpResponse

from .models import AMA, Question, Answer


def index(request):
    return HttpResponse("Hello, world. You're at the home page.")

def detail(request, ama_id):
    return HttpResponse("You're looking at AMA %s." % ama_id)

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )

from home.models import Question

from home.api.amas.permissions import IsOwnerOrReadOnly
from .serializers import (
    QuestionSerializer
    )


# class QuestionCreateAPIView(CreateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class QuestionDeleteAPIView(DestroyAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionDetailSerializer


class QuestionDetailAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# class QuestionUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionCreateUpdateSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )

from home.models import AMA
from .serializers import (
    AMACreateSerializer,
    AMADetailSerializer,
    AMASerializer,
    )


class AMACreateAPIView(CreateAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMACreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AMADeleteAPIView(DestroyAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMADetailSerializer


class AMADetailAPIView(RetrieveAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMASerializer


class AMAListAPIView(ListAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMASerializer


class AMAUpdateAPIView(UpdateAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMADetailSerializer

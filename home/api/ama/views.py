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

from home.models import AMA

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    AMACreateUpdateSerializer,
    AMADetailSerializer,
    AMASerializer,
    )


class AMACreateAPIView(CreateAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMACreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AMADeleteAPIView(DestroyAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMADetailSerializer


class AMADetailAPIView(RetrieveAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMADetailSerializer


class AMAListAPIView(ListAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMASerializer


class AMAUpdateAPIView(RetrieveUpdateAPIView):
    queryset = AMA.objects.all()
    serializer_class = AMACreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

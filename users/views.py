from rest_framework import viewsets, permissions, generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from materials.models import Course
from users.models import User, Subscription
from users.serializers import UserSerializer, RegisterSerializer, SubscriptionSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Защита CRUD операций

    def get_queryset(self):
        return User.objects.all()


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class SubscriptionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs['course_id'])
        serializer.save(user=self.request.user, course=course)
        return Response({"message": "Subscribed successfully."}, status=status.HTTP_201_CREATED)


class SubscriptionDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user, course_id=self.kwargs['course_id'])

    def destroy(self, request, *args, **kwargs):
        try:
            self.get_queryset().get().delete()
            return Response({"message": "Unsubscribed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({"message": "Not subscribed."}, status=status.HTTP_400_BAD_REQUEST)

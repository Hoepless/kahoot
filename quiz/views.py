from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import QuizSerializer, QuizTakerSerializer, QuizTakerDetailSerializer, QuizTakerResponseSerializer
from .models import Quiz, QuizTaker, QuizTakerResponse


class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated,)


class QuizTakerListView(generics.ListAPIView):
    queryset = QuizTaker.objects.all()
    serializer_class = QuizTakerSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('group',)
    search_fields = ('first_name', 'last_name', 'phone')


class QuizTakerDetailView(generics.RetrieveAPIView):
    queryset = QuizTaker.objects.all()
    serializer_class = QuizTakerDetailSerializer
    permission_classes = (IsAuthenticated,)


class QuizTakerResponseView(generics.CreateAPIView):
    queryset =  QuizTakerResponse.objects.all()
    serializer_class = QuizTakerResponseSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        QuizTakerResponse.calculate_final_score(**serializer.validated_data)


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
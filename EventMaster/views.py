from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from EventMaster.models import CategoryDb,EventDb
from django.shortcuts import get_object_or_404
from EventMaster.serializers import UserSerializer,CategorySerializer,EventSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import date
class SignUpView(APIView):
    def post(self, request):
        serializer_instance = UserSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(
                serializer_instance.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class UserListView(APIView):
    def get(self, request):
        qs = User.objects.all()
        serializer_instance = UserSerializer(qs, many=True)
        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )
class CategoryListCreateView(APIView):
    def get(self, request):
        qs = CategoryDb.objects.all()
        serializer_instance = CategorySerializer(qs, many=True)
        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )
    def post(self, request):
        serializer_instance = CategorySerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(
                serializer_instance.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class CategoryRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(CategoryDb, id=pk)
        serializer_instance = CategorySerializer(category)
        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )
    def put(self, request, pk):
        category = get_object_or_404(CategoryDb, id=pk)
        serializer_instance = CategorySerializer(
            category,
            data=request.data
        )
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(
                serializer_instance.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, pk):
        category = get_object_or_404(CategoryDb, id=pk)
        category.delete()
        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_200_OK
        )
class EventListCreateView(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = EventDb.objects.all()
        serializer_instance = EventSerializer(qs, many=True)

        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )
    def post(self, request):
        serializer_instance = EventSerializer(data=request.data)
        if serializer_instance.is_valid():
            if serializer_instance.validated_data['event_date'] < date.today():
                return Response(
                    {"error": "Event date cannot be in the past"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer_instance.save(
                created_by=request.user
            )
            return Response(
                serializer_instance.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class EventRetrieveUpdateDeleteView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # GET a particular event
    def get(self, request, pk):
        event = get_object_or_404(EventDb, id=pk)
        serializer_instance = EventSerializer(event)
        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )
    # UPDATE an event
    def put(self, request, pk):
        event = get_object_or_404(EventDb, id=pk)
        serializer_instance = EventSerializer(
            event,
            data=request.data
        )
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(
                serializer_instance.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_instance.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    # DELETE an event
    def delete(self, request, pk):
        event = get_object_or_404(EventDb, id=pk)
        event.delete()
        return Response(
            {"message": "Event deleted successfully"},
            status=status.HTTP_200_OK
        )

class EventByCategoryView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        category = get_object_or_404(CategoryDb, id=pk)
        qs = EventDb.objects.filter(category=category)
        serializer_instance = EventSerializer(qs, many=True)
        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )
class EventByDateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, event_date):
        qs = EventDb.objects.filter(event_date=event_date)
        serializer_instance = EventSerializer(qs, many=True)
        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )
class EventSearchView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        search = request.query_params.get('search')
        qs = EventDb.objects.filter(
            event_name__icontains=search
        )
        serializer_instance = EventSerializer(qs, many=True)
        return Response(
            serializer_instance.data,
            status=status.HTTP_200_OK
        )



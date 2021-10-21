from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import Chirp
from .forms import ChirpForm
from django.utils.http import is_safe_url
from django.conf import settings
from rest_framework import status
from .serializers import ChirpSerializer, ChirpActionSerializer, ChirpCreateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.

class ChirpsListView(APIView):
    
    def get(self, request, format=None):
        qs = Chirp.objects.all()
        serializer = ChirpSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, chirp_id):
        qs = Chirp.objects.get(id=chirp_id)
        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        qs = qs.filter(user=request.user)
        if not qs.exists():
            return Response({"message": "You cannot delete this Chirp"}, status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()
        obj.delete()
        return Response({"message": "Chirp deleted"}, status=status.HTTP_200_OK)

            
class ChirpActionView(APIView):
    """
    id is required.
    Chirp actions: like, unlike, rechirp.
    """

    def post(self, request, chirp_id, *args, **kwargs):
        serializer = ChirpActionSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            chirp_id = data.get("id")
            action = data.get("action")
            content = data.get("content")

        qs = Chirp.objects.filter(id=chirp_id)
        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = ChirpSerializer(obj)
            return Response({}, status=status.HTTP_200_OK)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "rechirp":
            new_chirp = Chirp.objects.create(user=request.user, 
                                                parent=obj,
                                                content=content)
            serializer = ChirpSerializer(new_chirp)
            Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Chirp liked"}, status=status.HTTP_200_OK)




    

# def chirp_create_view_pure(request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         if request.is_ajax():
#             return JsonResponse({}, status=401)
#         return redirect(settings.LOGIN_URL)
#     form = ChirpForm(request.POST or None)
#     next_url = request.POST.get("next")
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = request.user or None
#         obj.save()
#         if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
#             return redirect(next_url)
#         form = ChirpForm()
#     context = {
#         "form": form
#     }
#     return render(request, "components/form.html", context)
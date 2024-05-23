from django.shortcuts import render
from json import dumps, loads
from os import remove
from datetime import datetime
from rest_framework import exceptions, status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
# from .authentication import CustomAuth
from rest_framework.permissions import (SAFE_METHODS, AllowAny, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from account.models import User
from main.models import Course

def parseGet(request,kw):
    _ = request.query_params.get(kw)
    if _:
        return _
    else:
        return ""

# Create your views here.
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class WriteOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST']
    
class Post(APIView):
    # * allow get requests but authorize post/put/delete requests
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [TokenAuthentication]

    def get(self, format=None):
        ind = self.request.query_params.get("index")
        ind = int(ind) if ind is not None and ind != "" else 0
        filter = bool(self.request.query_params.get("filter"))
        if ind == -1:
            try:
                course_id = self.request.query_params.get("id")
                course = Course.objects.get(id=course_id)
                data = {}
                return Response(data)
            except Course.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif filter:
            keyword = parseGet(self.request,"search")
            query = Course.objects.filter(title__icontains=keyword)
            query2 = Course.objects.filter(tags__icontains=keyword)
            query = query | query2
            if query:
                data = {}
                return Response(data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            query = Course.objects.all()[ind:ind+30]
            if query:
                data = {}
                return Response(data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

    # ? These actions will be performed through the admin site
     
    # def post(self, request):
    #     try:
    #         data = loads(request.data["data"])
    #         token = request.headers["authorization"].split()[-1]
    #         userID = Token.objects.get(key=token).user.id
    #         userid = data["userid"]
    #         if userID == userid:
    #             title = data["title"]
    #             category = data["category"]
    #             subcategory = data["subcategory"]
    #             price = data["price"]
    #             state = data["state"]
    #             city = data["city"]
    #             locality = data["locality"]
    #             description = data["description"]
    #             tags = data["tags"]
    #             imageList = request.FILES.getlist("images")
    #             obj = Course.objects.create(title=title,
    #                                         userid=userid,
    #                                         category=category,
    #                                         subcategory=subcategory,
    #                                         price=price,
    #                                         state=state,
    #                                         city=city,
    #                                         locality=locality,
    #                                         description=description,
    #                                         tags=tags,
    #                                         )
    #             if imageList == []:
    #                 return Response({"error": "Product Images are required."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #             else:
    #                 path = []
    #                 for file in imageList:
    #                     name = main(file, userid)
    #                     path.append("media/images/"+name)
    #                 path = dumps(path)
    #                 obj.images = path
    #                 obj.save()
    #             return Response({f"Ad Posted successfully !"}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"error": "User Id mismatch."}, status=status.HTTP_401_UNAUTHORIZED)
    #     except Exception as e:
    #         print(e)
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     try:
    #         data = loads(request.data["data"])
    #         # print(data)
    #         obj = Course.objects.get(id=int(data["id"]))
    #         if obj.userid == int(data["userid"]):
    #             return Response({f"Post updated {obj.title}!"}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"error": "You are not authorized to change this post."}, status=status.HTTP_401_UNAUTHORIZED)
    #     except Exception as e:
    #         print(e)
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request):
    #     try:
    #         data = request.data
    #         obj = Course.objects.filter(id=data["id"])
    #         if obj.userid == data["userid"]:
    #             images = obj.images
    #             images = loads(images)
    #             for im in images:
    #                 remove(im)
    #             obj.delete()
    #             return Response("Post deleted successfully !", status=status.HTTP_200_OK)
    #         else:
    #             return Response({"error": "You are not authorized to delete this post !"}, status=status.HTTP_401_UNAUTHORIZED)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

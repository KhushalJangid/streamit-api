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
from account.models import Subscription, User
from main.models import Course, VideoAsset, Wishlist
from django.db.utils import IntegrityError

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
    

@api_view(['get'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_courses(request):
    offset_index = request.query_params.get("index")
    offset_index = int(offset_index) if offset_index is not None and offset_index != "" else 0
    filter = bool(request.query_params.get("filter"))
    if offset_index == -1:
        try:
            course_id = request.query_params.get("id")
            course = Course.objects.get(id=course_id)
            data = course.toJson()
            videos = VideoAsset.objects.filter(course=course)
            data["videos"] = [video.toJson() for video in videos]
            return Response(data)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif filter:
        keyword = parseGet(request,"search")
        query = Course.objects.filter(title__icontains=keyword)
        query2 = Course.objects.filter(tags__icontains=keyword)
        query = query | query2
        if query:
            data  = [q.toJson() for q in query]
            return Response(data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        query = Course.objects.all()[offset_index:offset_index+30]
        if query:
            data  = [q.toJson() for q in query]
            return Response(data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
@api_view(['get'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchased_courses(request):
    user = request.user
    query = Subscription.objects.filter(user=user)
    if query.exists():
        courses = [q.course.toJson() for q in query]
        return Response(courses)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['get'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_course(request,course_id):
    try:
        course = Course.objects.get(uniqueName=course_id)
        Subscription.objects.create(user=request.user,course=course)
        return Response(status=status.HTTP_202_ACCEPTED)
    except IntegrityError:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['get'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_videos(request,course_id):
    try:
        course = Course.objects.get(uniqueName=course_id)
        query = VideoAsset.objects.filter(course=course)
        videos = [q.toJson() for q in query]
        return Response(videos)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['get'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def whishlist(request):
    try:
        items = Wishlist.objects.filter(user=request.user)
        if items.exists():
            courses = [item.course.toJson() for item in items ]
            return Response(courses)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
    
@api_view(['post'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_whishlist(request,courseId):
    try:
        course = Course.objects.get(uniqueName=courseId)
        Wishlist.objects.create(user=request.user,course=course)
        return Response(status=status.HTTP_200_OK)
    except IntegrityError:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
    
    
@api_view(['post'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_whishlist(request,courseId):
    try:
        course = Course.objects.get(uniqueName=courseId)
        Wishlist.objects.delete(user=request.user,course=course)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['get'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_video(request,course_id,video_id):
    try:
        user = request.user
        course = Course.objects.get(uniqueName=course_id)
        if course.price != 0:
            subscription = Subscription.objects.filter(user=user,course=course)
            if subscription.exists():
                query = VideoAsset.objects.get(uniqueName=video_id)
                return Response({"dataUrl":query.raw.url})
            else:
                return Response({"error":"Course not purchased"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            query = VideoAsset.objects.get(uniqueName=video_id)
            return Response({"dataUrl":query.raw.url})
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except VideoAsset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

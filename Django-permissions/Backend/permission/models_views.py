# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Course


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_course(request):
    if not request.user.has_perm("permission.add_course"):
        return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"create successfully"}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_courses(request):
    if not request.user.has_perm("permission.view_course"):
        return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    
    return Response({"message":"fetch successfully"}, status=status.HTTP_200_OK)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_course(request):
    if not request.user.has_perm("permission.change_course"):
        return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"updated successfully"}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_course(request):
    if not request.user.has_perm("permission.delete_course"):
        return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"deleted successfully"}, status=status.HTTP_204_NO_CONTENT)





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_subject(request):
    if not request.user.has_perm("permission.add_subject"):
        return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"create successfully"}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_subjects(request):
    if not request.user.has_perm("permission.view_subject"):
        return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"fetch successfully"}, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_subject(request):
    if not request.user.has_perm("permission.change_subject"):
         return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"updated successfully"}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_subject(request):
    if not request.user.has_perm("permission.delete_subject"):
         return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"deleted successfully"}, status=status.HTTP_204_NO_CONTENT)





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_book(request):
    if not request.user.has_perm("permission.add_book"):
         return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    return Response({"message":"create successfully"}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_books(request):
    if not request.user.has_perm("permission.view_book"):
         return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"fetch successfully"}, status=status.HTTP_200_OK)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_book(request):
    if not request.user.has_perm("permission.change_book"):
         return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"updated successfully"}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_book(request):
    if not request.user.has_perm("permission.delete_book"):
         return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response({"message":"deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



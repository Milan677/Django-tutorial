from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import AdminRegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


@api_view(["POST"])
@permission_classes([AllowAny])  # restrict later if needed
def register_admin(request):
    serializer = AdminRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    password = data.pop("password")

    # Ensure admin group exists
    admin_group, _ = Group.objects.get_or_create(name="admin")

    # Optional: prevent multiple admins (remove if not needed)
    # if User.objects.filter(groups=admin_group).exists():
    #     return Response(
    #         {"error": "Admin already exists"},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    with transaction.atomic():
        user = User.objects.create(**data, is_staff=True, is_superuser=False)
        user.set_password(password)
        user.save()
        user.groups.add(admin_group)

    return Response(
        {
            "message": "Admin registered successfully",
            "admin": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": "admin"
            }
        },
        status=status.HTTP_201_CREATED
    )

# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.db import transaction
from .serializers import UserRegisterSerializer
from .models import User

@api_view(["POST"])
@permission_classes([AllowAny])  # restrict later if needed
def register_user(request):
    """
    Register a teacher or student based on role field
    POST payload example:
    {
        "username": "teacher1",
        "email": "teacher1@test.com",
        "password": "Teacher@123",
        "role": "teacher"
    }
    """
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    password = data.pop("password")
    role = data.pop("role")

    # Validate role
    if role not in ["teacher", "student"]:
        return Response({"error": "Invalid role"}, status=400)

    # Ensure group exists
    group, _ = Group.objects.get_or_create(name=role)

    with transaction.atomic():
        user = User.objects.create(**data, is_active=True)
        user.set_password(password)
        user.save()
        user.groups.add(group)

    return Response(
        {
            "message": f"{role.capitalize()} registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": role
            }
        },
        status=201
    )



@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Get role (group)
    group = user.groups.first()
    role = group.name if group else None

    # JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": role,
                "permissions": list(user.get_all_permissions()),
            }
        },
        status=status.HTTP_200_OK
    )

from django.contrib.auth.models import Permission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def list_permissions_by_model(request):
    ALLOWED_APPS = ["permission"]  # 👈 your apps only

    data = {}

    permissions = (
        Permission.objects
        .select_related("content_type")
        .filter(content_type__app_label__in=ALLOWED_APPS)
    )

    for perm in permissions:
        model = perm.content_type.model  # course, book
        app = perm.content_type.app_label

        if model not in data:
            data[model] = {
                "app": app,
                "permissions": []
            }

        action = perm.codename.split("_")[0]  # add/view/change/delete

        data[model]["permissions"].append({
            "id": perm.id,
            "action": action,
            "codename": perm.codename,
            "name": perm.name
        })

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def list_users(request):
    users = User.objects.all()

    data = []
    for user in users:
        group = user.groups.first()
        role = group.name if group else None
        data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role
        })

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def user_permissions(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Role
    group = user.groups.first()
    role = group.name if group else None

    # User permissions (includes group permissions)
    user_perms = user.get_all_permissions()  # Returns 'app_label.codename'

    # Grouped by model
    data = {}
    for perm in Permission.objects.select_related("content_type").all():
        model_name = perm.content_type.model
        app_label = perm.content_type.app_label

        if model_name not in data:
            data[model_name] = {
                "app": app_label,
                "permissions": []
            }

        data[model_name]["permissions"].append({
            "id": perm.id,
            "codename": perm.codename,
            "name": perm.name,
            "assigned": f"{app_label}.{perm.codename}" in user_perms
        })

    return Response({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role
        },
        "permissions": data
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def update_user_permissions(request, user_id):
    """
    Update permissions for a user.
    Expects payload: { "permissions": [1,2,3] }  # list of permission IDs
    """
    user = get_object_or_404(User, id=user_id)
    permission_ids = request.data.get("permissions", [])

    if not isinstance(permission_ids, list):
        return Response({"error": "permissions must be a list of IDs"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch Permission objects from IDs
    permissions = Permission.objects.filter(id__in=permission_ids)

    with transaction.atomic():
        # Clear existing user-specific permissions
        user.user_permissions.clear()
        # Assign new permissions
        user.user_permissions.add(*permissions)

    return Response({"message": "Permissions updated successfully"})

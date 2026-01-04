from django import views
from django.urls import path
from .views import *
from .models_views import *

urlpatterns = [
    path("register/admin/", register_admin),
    path("register/user/", register_user, name="register_user"),
    path("login/", login),
    path("permissions/", list_permissions_by_model),
    path("users/", list_users),
    path("users/<uuid:user_id>/permissions/list/", user_permissions),
    path("users/<uuid:user_id>/permissions/add/", update_user_permissions),

    path("course/", list_courses),
    path("course/create/", create_course),
    path("course/update/", update_course),
    path("course/delete/", delete_course),

    path("subject/", list_subjects),
    path("subject/create/", create_subject),
    path("subject/update/", update_subject),
    path("subject/delete/", delete_subject),

    path("book/", list_books),
    path("book/create/", create_book),
    path("book/update/", update_book),
    path("book/delete/", delete_book),
]

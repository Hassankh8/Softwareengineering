import random
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import MediaItem, SearchHistory, User
from core.serializers import RegisterUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import urllib.parse


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view"})


def home_view(request):
    return render(request, "login.html")


def login_view(request):
    return render(request, 'login.html') 


def main(request):
    return render(request, "main.html")


def user_list(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, "user_list.html", {"users": users})


def delete_search(request, search_id):
    if request.method == "POST":
        # Use get_object_or_404 to raise a 404 if the SearchHistory does not exist
        search = get_object_or_404(SearchHistory, id=search_id)

        # Delete the search object
        search.delete()

        # Redirect back to the previous page or to a default location
        redirect_url = request.META.get("HTTP_REFERER", reverse("media_search"))
        return HttpResponseRedirect(redirect_url)


def update_search(request, search_id):
    if request.method == "POST":
        # Get the search object or handle the error
        search = get_object_or_404(SearchHistory, id=search_id)

        # Collect the form data
        data = collect_form_data(request)

        # Update the search object if data is provided
        update_search_fields(search, data)

        # Save the updated search object
        search.save()

    return HttpResponseRedirect(
        request.META.get("HTTP_REFERER", reverse("media_search"))
    )


def collect_form_data(request):
    """Collect and return the form data."""
    query = request.POST.get("query")
    media_type = request.POST.get("media_type")
    return {"query": query, "media_type": media_type}


def update_search_fields(search, data):
    """Update the search object fields if data is provided."""
    if data.get("query"):
        search.query = data["query"]
    if data.get("media_type"):
        search.media_type = data["media_type"]


def search_history_view(request):
    search_history = fetch_user_search_history(request)
    return render(request, "search_history.html", {"search_history": search_history})


def fetch_user_search_history(request):
    """Extract user ID from request and return search history if user exists."""
    uid = request.GET.get("user_id")
    if not uid:
        return []

    user = get_user_by_id(uid)
    if not user:
        return []

    return SearchHistory.objects.filter(user=user).order_by("-searched_at")


def get_user_by_id(user_id):
    """Attempt to get the user by ID, return None if not found."""
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


@api_view(["POST", "GET"])
def signup(request):
    if request.method == "POST":
        print("SIGNUP VIEW HIT")

        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": 200, "message": "User created successfully"}, status=200
            )
        else:
            return Response({"status": 400, "message": serializer.errors}, status=400)

    else:
        return render(request, "signup.html")


# User Login API View
@api_view(["POST", "GET"])
def login(request):
    print("loginapo sajdjsa")
    if request.method == "POST":
        user_email = request.data.get("user_email")
        user_password = request.data.get("user_password")

        # Check if email and password are provided
        if not user_email or not user_password:
            return Response(
                {"status": 400, "message": "Please provide both email and password"},
                status=400,
            )

        try:
            # Check if user exists
            user = User.objects.get(user_email=user_email)

            # Check if password is correct
            if check_password(user_password, user.user_password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response(
                    {
                        "status": 200,
                        "message": "Login successful",
                        "access_token": access_token,
                        "user_id": user.id,
                    },
                    status=200,
                )
            else:
                return Response(
                    {"status": 401, "message": "Invalid credentials"}, status=401
                )

        except User.DoesNotExist:
            return Response({"status": 404, "message": "User not found"}, status=404)

    else:
        return render(request, "login.html")


@api_view(["PUT", "DELETE"])
def update_delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        # Anyone logged in can update or delete users now
        if request.method == "PUT":
            user_name = request.data.get("user_name")
            user_email = request.data.get("user_email")
            user_password = request.data.get("user_password")

            if user_name:
                user.user_name = user_name
            if user_email:
                user.user_email = user_email
            if user_password:
                user.user_password = make_password(user_password)

            user.save()

            return Response({"status": 200, "message": "User updated successfully"})

        elif request.method == "DELETE":
            user.delete()
            return Response({"status": 200, "message": "User deleted successfully"})

    except User.DoesNotExist:
        return Response({"status": 404, "message": "User not found"})
    except Exception as e:
        return Response({"status": 500, "message": str(e)})


def media_search(request):
    context = prepare_search_context(request)

    if context.get("error"):
        return render(request, "media_search.html", context)

    user_id = request.GET.get("user_id")
    if user_id and context["query"]:
        log_user_search(
            user_id, context["query"], context["media_type"], context["media_items"]
        )

    return render(request, "media_search.html", context)


def prepare_search_context(request):
    query = request.GET.get("query", "")
    media_type = request.GET.get("media_type", "image")
    encoded_query = urllib.parse.quote(query)
    page_number = random.randint(1, 5)

    print("Query received:", query)
    print("User ID:", request.GET.get("user_id"))

    api_url = build_openverse_url(media_type, encoded_query, page_number)
    print("Requesting from:", api_url)

    response = requests.get(api_url, headers={"User-Agent": "MediaSearchApp/1.0"})

    if response.status_code != 200:
        return {
            "media_items": [],
            "query": query,
            "media_type": media_type,
            "error": "Unable to retrieve media items at this time.",
        }

    results = response.json().get("results", [])
    return {"media_items": results, "query": query, "media_type": media_type}


def build_openverse_url(media_type, encoded_query, page):
    base_api = "https://api.openverse.org/v1"
    endpoint = "images" if media_type == "image" else "audio"
    license_param = "license_type=all"

    if media_type == "image":
        return f"{base_api}/{endpoint}?q={encoded_query}&page={page}&{license_param}&size=medium"
    return f"{base_api}/{endpoint}?q={encoded_query}&page={page}&{license_param}"


def log_user_search(user_id, query, media_type, items):
    try:
        user = User.objects.get(id=user_id)
        SearchHistory.objects.create(user=user, query=query, media_type=media_type)

        for entry in items:
            MediaItem.objects.create(
                user=user,
                query=query,
                media_type=media_type,
                url=entry.get("url", ""),
                title=entry.get("title", ""),
                thumbnail=entry.get("thumbnail", ""),
            )
    except User.DoesNotExist:
        print(f"User with ID {user_id} not found.")

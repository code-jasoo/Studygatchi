from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import StudyUser, Task  # TODO remove, should be serializer
from .serializers import TaskSerializer


@api_view(["GET"])
def ping(_request: Request) -> Response:
    print(type(StudyUser))
    return Response("pong")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request: Request) -> Response:
    serializer = TaskSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        # save and return
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task(request: Request) -> Response:
    username = request.query_params.get("username")
    if not username:
        return Response({"error": "No username provided"}, status=status.HTTP_400_BAD_REQUEST)

    # look up user and react accordingly if they don't exist
    try:
        user: StudyUser = StudyUser.objects.get(username=username)
        tasks: QuerySet[Task] = Task.objects.filter(user=user)

        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except StudyUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def edit_task(request: Request, pk: int) -> Response:
    # Attempt to edit the task
    try:
        # Query the task with the primary key but also the foreign key
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task does not exist for authenticated user"}, status=status.HTTP_404_NOT_FOUND)

    # Create serializer with the current task object, but update with the given request data. Use partial to tell django
    # that it can accept partial data/params.
    serializer = TaskSerializer(task, data=request.data, partial=True)

    # Validate the data is correct
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Ship it.
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

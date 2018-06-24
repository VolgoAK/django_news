# Create your views here.
import os

from rest_framework import status, permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def posts(request):
    if request.method == "GET":
        posts = Post.objects.order_by('-pub_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def private_posts(request):
    posts = Post.objects.order_by('-pub_date')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def post_by_id(requst, id):
    try:
        post = Post.objects.get(pk=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((AllowAny,))
def add_claps(request):
    claps = request.data['value']
    id = request.data['post_id']
    try:
        post = Post.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    post.votes += claps
    post.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def comments(request, id):
    if request.method == 'GET':
        commentss = Comment.objects.filter(post__id=id).order_by('-pub_date')
        serializer = CommentSerializer(commentss, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        request.data['post'] = id
        serializer = CommentSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def loadImage(request, id):
    try:
        post = Post.objects.get(pk=id)
    except:
        return Response("Post with {} does not exists".format(id), status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['image']
    extension = file.name.split('.')[-1]
    if not (extension in ['jpg', 'png']):
        return Response("incorrect image file", status=status.HTTP_400_BAD_REQUEST)

    # create directory if not exists
    path = 'static/media/'
    try:
        os.makedirs(path)
    except:
        pass

    filename = "post_title_img_{}.{}".format(id, extension)

    # write file to the static storage
    with open(path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # link file to the related post object
    post.image = filename
    post.save()

    return Response(status=status.HTTP_201_CREATED)

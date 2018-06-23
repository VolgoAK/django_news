# Create your views here.
from rest_framework import status
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
        return Response(serializer)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((AllowAny))
def comments(request, id):
    commentss = Comment.objects.filter(post__id=id).order_by('-pub_date')
    serializer = CommentSerializer(commentss, many=True)
    return Response(serializer)

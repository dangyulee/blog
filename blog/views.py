from .models import Blog
from .serializers import BlogSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

'''
전체 블로그를 조회
'''


class BlogList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST']) # GET 요청만 받겠다.    
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def blog_list(request):
#     if request.method == 'GET':
#         blogs = Blog.objects.all()
#         serializer = BlogSerializer(blogs, many=True) # Blog 모델들을 직렬화할 수 있다.
#         return Response(serializer.data, status=status.HTTP_200_OK) # 직렬화된 데이터(serializer.data)를 가지고 Response 만들어서 반환
#     elif request.method == 'POST':
#         serializer = BlogSerializer(data=request.data) # 요청 데이터(request.data)를 가지고 역직렬화를 수행해줄 수 있다.
#         if serializer.is_valid(): # 유효성 검사
#             serializer.save() # 역직렬화해서 만들어낸 Blog 모델을 저장한다.
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#     return Response(status=status.HTTP_400_BAD_REQUEST)

'''
한 블로그 조회
'''
class BlogDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        blog = get_object_or_404(Blog, pk=pk)
        return blog

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsOwnerOrReadOnly])
# def blog_detail(request, pk): # 요청 데이터와 함께 pk값도 url을 통해 받겠다
#     try: # 아래 코드를 시도
#         blog = Blog.objects.get(pk=pk) # 해당 pk에 해당하는 Blog 객체를 찾는다
#         if request.method == 'GET':
#             serializer = BlogSerializer(blog) # Blog 모델을 직렬화할 수 있다.
#             return Response(serializer.data, status=status.HTTP_200_OK) # 직렬화된 데이터(serializer.data)를 가지고 Response 만들어서 반환
#         elif request.method == 'PUT':
#             serializer = BlogSerializer(blog, data=request.data) # Create 때와 다른 부분
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(status=status.HTTP_200_OK)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         elif request.method == 'DELETE':
#             blog.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#     except Blog.DoesNotExist: # 예외(오류) 발생 시 아래 코드 실행
#         return Response(status=status.HTTP_404_NOT_FOUND)
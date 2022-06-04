from rest_framework.generics import *
from activity.views import IsGETOrIsAuthenticated
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .serilaizers import *
from .models import *

class AboutUsListAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()[:1]

class AboutUsCreateAPI(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()

class AboutUsReadAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()
    lookup_field = "pk"
    

class BannerListAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()[:1]

class BannerCreateAPI(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()

class BannerReadAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()
    lookup_field = "pk"

class SupportQueryAPI(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SupportQuerySerializer
    queryset = SupportQuery.objects.all()


class BlogListAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

class BlogCreateAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

class BlogReadAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = "pk"

    




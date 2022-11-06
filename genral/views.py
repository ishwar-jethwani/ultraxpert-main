from rest_framework.generics import *
from activity.views import IsGETOrIsAuthenticated
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .serilaizers import *
from .models import *

class AboutUsListAPI(ListAPIView):
    """List APIView For Dispalying About Us Info"""
    permission_classes = [AllowAny]
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()[:1]

class AboutUsCreateAPI(CreateAPIView):
    """Create APIView For Creating About Us Info"""
    permission_classes = [IsAdminUser]
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()

class AboutUsReadAPI(RetrieveUpdateDestroyAPIView):
    """For Retrieving Updating And Deleting About Us Info"""
    permission_classes = [IsAdminUser]
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()
    lookup_field = "pk"
    

class BannerListAPI(ListAPIView):
    """List APIView For Displaying Banner)"""
    permission_classes = [AllowAny]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()[:1]

class BannerCreateAPI(CreateAPIView):
    """Create APIView For Creating New Banner"""
    permission_classes = [IsAdminUser]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()

class BannerReadAPI(RetrieveUpdateDestroyAPIView):
    """For Retrieving Updating And Deleting Banner Info"""
    permission_classes = [IsAdminUser]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()
    lookup_field = "pk"

class SupportQueryAPI(CreateAPIView):
    """Create APIView For Creating Support Query"""
    permission_classes = [AllowAny]
    serializer_class = SupportQuerySerializer
    queryset = SupportQuery.objects.all()


class BlogListAPI(ListAPIView):
    """List APIView For Displaying Blog List)"""
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

class BlogCreateAPI(CreateAPIView):
    """Create APIView For Creating New Blog"""
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

class BlogReadAPI(RetrieveUpdateDestroyAPIView):
    """For Retrieving Updating And Deleting Blog"""
    permission_classes = [IsAdminUser]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = "pk"

    




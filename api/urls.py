from django.urls import path, include
# from rest_framework import routers
# from django.conf.urls import url
# from rest_framework_swagger.views import get_swagger_view
from .views import *

# router = routers.DefaultRouter()
# router.register(r'user/<str:username>/profile/', UserProfileModelViewSet)

# schema_view = get_swagger_view(title='Bromine API')

urlpatterns = [
    path('user/<str:username>/profile', UserProfileModelViewSet.as_view()),
    path('blogs/', BlogListView.as_view()),
    path('blogs/<slug>/', PostView.as_view()),
    path('create/blog/', CreateBlogPostView.as_view()),
    path('blogs/<slug>/comments/<uuid>', CommentDetailView.as_view(), name='tippani-retrieve-destroy'),
    path('blogs/<slug>/comments/', CommentListView.as_view(), name='tippani-list-create'),
    # path('docs/', schema_view)
]
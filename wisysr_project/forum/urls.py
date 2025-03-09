from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TopicViewSet
from django.urls import path
from .views import home, category_topics, topic_detail

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'topics', TopicViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', home, name='home'),
    path('', home, name='home'),
    path('category/<int:category_id>/', category_topics, name='category_topics'),
    path('topic/<int:topic_id>/', topic_detail, name='topic_detail'),
]

from rest_framework import viewsets
from .serializers import CategorySerializer, TopicSerializer
from django.shortcuts import render, get_object_or_404
from .models import Category, Topic
from django.shortcuts import redirect
from .forms import CommentForm

def home(request):
    categories = Category.objects.all()
    topics = Topic.objects.all().order_by('-created_at')[:5]
    return render(request, 'forum/index.html', {'categories': categories, 'topics': topics})

def category_topics(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = Topic.objects.filter(category=category)
    return render(request, 'forum/category_topics.html', {'category': category, 'topics': topics})

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, 'forum/topic_detail.html', {'topic': topic})


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    comments = topic.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = CommentForm()

    return render(request, 'forum/topic_detail.html', {'topic': topic, 'comments': comments, 'form': form})
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

from rest_framework import viewsets
from .serializers import CategorySerializer, TopicSerializer
from django.shortcuts import get_object_or_404
from .models import Category, Topic
from .forms import CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UploadedImage
from .forms import ImageUploadForm


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


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def index(request):
    return render(request, "index.html")

def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user  # Привязываем к текущему пользователю
            image.save()
            return redirect("gallery")  # Перенаправление на страницу с загруженными файлами
    else:
        form = ImageUploadForm()
    return render(request, "upload_image.html", {"form": form})

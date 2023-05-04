from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.http import HttpResponse

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView

from .models import Circle, Friend_Request

from .forms import CommentForm

# Create your views here.

# Class Based Views

class CircleCreate(LoginRequiredMixin,  CreateView):
    model = Circle
    fields = ['title', 'creator', 'description', 'tags']

    # Interrupt normal form_valid functionality to assign user
    def form_valid(self, form):
        # Assign logged in user
        form.instance.user = self.request.user
        # Allow CreateView to continue
        return super().form_valid(form)
    
class CircleUpdate(LoginRequiredMixin,  UpdateView):
    model = Circle
    fields = ['title', 'creator', 'description', 'tags']

class CircleDelete(LoginRequiredMixin,  DeleteView):
    model = Circle
    success_url = "/circles"

# Function Views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def circles_index(request):
    circles = Circle.objects.filter(user=request.user)
    allUsers = User.objects.all()
    return render(request, 'circles/index.html', 
                  { 'circles': circles,
                   'allUsers':  allUsers})

@login_required
def circle_detail(request, circle_id):
    circle= Circle.objects.get(id=circle_id)
    comment_form = CommentForm()
    comments = circle.comments.all()
    return render(request, 'circles/detail.html', 
                  { 'circle': circle, 
                    'comment_form': comment_form, 
                    'comments': comments })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid signup - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_comment(request, circle_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.circle_id = circle_id
    u = request.user
    new_comment.user_id = u.id
    new_comment.save()
  return redirect('detail', circle_id=circle_id)

@login_required
def send_friend_request(request, userID):
   from_user = request.user.profile
   to_user = User.objects.get(id=userID).profile
   friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
   if created:
      return HttpResponse('Friend request sent')
   else:
      return HttpResponse('Friend request was already sent')
   
@login_required
def accept_friend_request(request, requestID):
   friend_request = Friend_Request.objects.get(id=requestID)
   if friend_request.to_user == request.user:
      friend_request.to_user.profile.friends.add(friend_request.from_user)
      friend_request.from_user.profile.friends.add(friend_request.to_user)
      friend_request.delete()
      return HttpResponse('Friend Request Accepted')
   else:
      return HttpResponse('You did not accept')
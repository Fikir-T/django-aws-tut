from django.shortcuts import render, redirect , HttpResponse ,get_object_or_404
from .forms import SignUpForm
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from shop.models import Category , Item
from .models import UserActivity
from  django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    category = Category.objects.all()[0:10]
    item = Item.objects.filter(is_sold=False)
    context = {
        'category':category ,
        'item':item,
    }
    return render(request, 'main/index.html',context)

def filter_items(request):
    selected_category_ids = request.GET.getlist('category_ids')

    items = Item.objects.filter(is_sold=False)

    if selected_category_ids:
        for cat_id in selected_category_ids:
            items = items.filter(item_category__CategoryId=cat_id)

    context = {
        'item': items,
    }
    return render(request, 'main/partials/filter.html', context)

def aboutus(request):
    return render(request, 'main/aboutus.html')

def signup(request):
    if request.method == 'POST':
        form= SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('main:login')
    else:
        form = SignUpForm()
    context = {
        'form':form
    }
    return render(request, 'main/signup.html',context)

def login(request):
    return render(request, 'main/login.html')
@login_required
def logout(request):
    logout(request)
    return redirect('main:index')
@login_required
# @csrf_exempt
def profile(request,pk):
    user =get_object_or_404(User, pk=pk)
    online = UserActivity.objects.filter(user=user).first()
    # print(online)
    
    context =  {

        'user':user,
        'online':online
    }
    if request.user != user :
        raise PermissionDenied
    else:
        return render(request, 'main/profile.html',context)

    


def success(request):
    return render(request, 'main/success.html')


@login_required
@csrf_exempt
def update_last_seen(request):
    activity, _ = UserActivity.objects.get_or_create(user=request.user)
    activity.last_seen = timezone.now()
    activity.save(update_fields=['last_seen'])
    return HttpResponse(status=204)

def superuser_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view  #I need to understand this custom decorator if I'm gonna be a django develoer sometime soon and work on my own decorators because decorators are so cool.


@superuser_required
def visitors(request):
    Online = UserActivity.objects.all()

    context = {
        'Online':Online,
    }
    return render (request , 'main/visitors.html',context)


#below this is a written a hokum, because i'm in denial of using react and still trying to understand and use

# @superuser_required
def visitors_json(request):


    from django.http import JsonResponse
    from django.forms.models import model_to_dict
    online_users = UserActivity.objects.all()

    data = {
        "online": [model_to_dict(user) for user in online_users]
    }

    return JsonResponse(data, safe=False)

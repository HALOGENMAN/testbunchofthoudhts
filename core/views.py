from django.shortcuts import render,redirect
from core.models import Journal,Categories
from django.db.models import Q
from django.contrib.auth.models import User,auth
from django.contrib import messages

def is_valid_qureyparameter(pram):
    return pram !="" and pram is not None

def BootstrapFilterView(request):
    qs = Journal.objects.all()
    categories = Categories.objects.all()
    title_contains_query=request.GET.get("title_contains")
    title_exact_query=request.GET.get("title_exact")
    title_author_query=request.GET.get("title_author")
    MAX_VIEW_COUN = request.GET.get("MAX_VIEW_COUN")
    MIN_VIEW_COUN = request.GET.get("MIN_VIEW_COUN")
    date_min = request.GET.get("date_min")
    date_max = request.GET.get("date_max")
    title_categories = request.GET.get("title_categories")
    reviewed = request.GET.get("reviewed")
    not_reviewed = request.GET.get("not_reviewed")
   
    if is_valid_qureyparameter(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    elif is_valid_qureyparameter(title_exact_query):
        qs = qs.filter(id=title_exact_query)
    
    elif is_valid_qureyparameter(title_author_query):
        qs = qs.filter(Q(title__icontains=title_author_query) | Q(author__name__icontains=title_author_query)).distinct()
    
    if is_valid_qureyparameter(MIN_VIEW_COUN):
        qs = qs.filter(views__gte=MIN_VIEW_COUN)

    if is_valid_qureyparameter(MAX_VIEW_COUN):
        qs = qs.filter(views__lt=MAX_VIEW_COUN)

    if is_valid_qureyparameter(date_min):
        qs = qs.filter(publish_date__gte=date_min)

    if is_valid_qureyparameter(date_max):
        qs = qs.filter(publish_date__lt=date_max)
    
    if is_valid_qureyparameter(title_categories) and title_categories != "Choose....":
        qs = qs.filter(categories__name=title_categories)

    if reviewed == "on":
        qs = qs.filter(reviewed=True)
    
    elif not_reviewed == "on":
        qs = qs.filter(reviewed=False)

        
    context ={
        "queryset":qs,
        "categories":categories
    }
    
    return render(request,"home.html",context)
def dashbord(request):
    return render(request,"dashbord.html")


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if request.method == "POST":
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.info(request,"not able to do")
            return render(request,"dashbord.html")
        else:
            messages.info(request,"user is not exist ")
            return render(request,"index.html")
    else:
        return render(request,"index.html")

def create(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    if request.method == "POST":
        if password1 == password2:
            if User.objects.filter(username = username).exists() and User.objects.filter(email = email).exists():
                messages.info(request,"USERNAME EXIST or EMAIL EXIST")
                return render(request,"create.html")
            else:
                user = User.objects.create_user(username = username,email=email,password=password1)
                user.save()
                return redirect("login")
        else:
            messages.info(request,"password did not match")
            return render(request,"create.html")
    else:
            
            return render(request,"create.html")

    
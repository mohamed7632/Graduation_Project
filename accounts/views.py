from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from .forms import CustomUserForm
from .models import CustomUser,Topic
import requests
from django.contrib.auth.decorators import login_required
from . import DataRetrieval as dr
from . import Analysis as analysis
from . import SentimentModel as sentiment
from sklearn.pipeline import Pipeline
from joblib import load
import json
from . import AspectsAnalysis as AS
from django.contrib import messages
#pipeline = load("visionalyst_classifier_dt.joblib")

# Create your views here.
@login_required(login_url="/accounts/login/")
def home_page(request):
    return render(request,'home.html')

def get_data(request):
    if request.method == 'POST':
         data = request.POST['search']
         request.session['search']=data
    else:
        data=request.session.get('search','unknown')
    # obj=dr.DataRetrieval()
    # res=obj.get_all_reviews(data)

    # res=sentiment.SentimentModel.get_sentiment(res)
    # js = res.to_json(orient = 'records' , date_format = 'iso')
    # request.session['res']=js
    if not request.session['search']:
       
        return render(request,'home.html')
    else:
          
         return dashboard(request,data)
    

@login_required(login_url="/accounts/login/")
def tweets(request):
  #response=requests.get('https://api.covid19api.com/countries').json()
  response=request.session.get('res','unknown')
  search=request.session.get('search','unknown')
  res = json.loads(response)
  print(type(res))
  return render(request,'tweets.html',{'search':search,'response':res })

 

@login_required(login_url="/accounts/login/")
def dashboard(request,data):
    #res=request.session.get('res','unknown')
    obj=dr.DataRetrieval()
    res=obj.get_all_reviews(data)
    hashtag,hash_count=analysis.Analysis.hashtag_analysis(res)
    
    top_hash_count=max(hash_count)
    top_hash=hashtag[hash_count.index(top_hash_count)]
    
    
    location,loc_count = [],[]
    location,loc_count=analysis.Analysis.location_analysis(res)
    top_loc_count=max(loc_count)
    top_location=location[loc_count.index(top_loc_count)]
    
    #labels_wordcloud, counts_wordlcoud =analysis.Analysis.wordcloud(res)
    res = sentiment.SentimentModel.get_sentiment(res)
    
    sent , sent_count = sentiment.SentimentModel.count_sentiment(res)
    
    labels_positive, counts_positive, labels_negative, counts_negative = analysis.Analysis.line_analysis(res)
    #print(labels_positive, counts_positive, labels_negative, counts_negative)
    # print(labels_positive,counts_positive, labels_negative, counts_negative)
    search=request.session.get('search','unknown')
    js = res.to_json(orient = 'records' , date_format = 'iso')
    request.session['res']=js
    obj=AS.AspectsAnalysis()
    # print(search) 
    noun, pos, neg=obj.get_aspects(res)
    top_aspects_count = max(pos)
    top_aspect = noun[pos.index(top_aspects_count)]
#'labels_wordcloud':labels_wordcloud,'counts_wordlcoud':counts_wordlcoud,
    context={'hashtag':hashtag,'hash_count':hash_count,'top_hash':top_hash,'top_hash_count':top_hash_count,
    'top_location':top_location,'top_loc_count':top_loc_count,
    'location':location,'loc_count':loc_count,'sent':sent,'sent_count':sent_count
    ,'labels_positive':labels_positive,'counts_positive': counts_positive,
     'labels_negative':labels_negative, 'counts_negative':counts_negative,
     'noun':noun,'pos': pos,'neg': neg,'top_aspects_count':top_aspects_count,'top_aspect':top_aspect,
     'search':search}
    return render(request,"dashboard.html",context) 


def signup(request):
    
    if request.method=="POST":
            user_form=CustomUserForm(request.POST)        
            if  user_form.is_valid():
                user_form.save()
                username=user_form.cleaned_data['username']
                password=user_form.cleaned_data['password1']
                user=authenticate(username=username,password=password)
                login(request,user)
                return render(request,'home.html')
            

    else:
            user_form=CustomUserForm()
            

    context={'user':request.user,'user_form':user_form}
    return render(request,'registration/signup.html',context)

def create_report(request,topic):
    request.session['search']=topic
    return get_data(request)
    
# def user_login(request):
    # if request.method == 'POST':
    #     # Process the request if posted data are available
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     # Check username and password combination if correct
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         # Save session as cookie to login the user
    #         login(request, user)
    #         # Success, now let's login the user.
    #         return render(request, 'profile.html')
    #     else:
    #         # Incorrect credentials, let's throw an error to the screen.
    #         return render(request, 'registration/login.html', {'error_message': 'Incorrect username and / or password.'})
    # else:
    #     # No post data availabe, let's just show the page to the user.
    #     return render(request, 'registration/login.html')   

@login_required(login_url="/accounts/login/")
def profile(request):
    user=request.user
    #profile=Profile.objects.get(user=request.user)
    #user=CustomUserForm.objects.all()
    #user=CustomUser.objects.get(user=request.user)
    #profile=Profile.objects.all()
    context={'user':user}
    return render(request,"profile.html",context)

def save_topic(request,topic):
    user=request.user
    new_user=CustomUser.objects.get(username=user.username)
    #topics_list=Topic.objects.all()
    topics_list=new_user.topics.all()
    new_topic=Topic()
    new_topic.topic_name=topic
    llist = []
    for t in topics_list:
        llist.append(t.topic_name)
    if topic in llist:
        print('ohhh')
        # new_topic.save()
        # new_user.topics.add(new_topic)
        # new_user.save()
    else:
        new_topic.save()
        new_user.topics.add(new_topic)
        new_user.save()
         


  
         
        
    
    # user=request.user
    # new_user=CustomUser.objects.get(username=user.username)
    # new_topic=Topic()
    # new_topic.topic_name=topic
    # new_topic.save()
    # new_user.topics.add(new_topic)
    # new_user.save()
    return render(request,'profile.html')

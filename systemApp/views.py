from django.shortcuts import render
import requests
from . import DataRetrieval as dr
from . import Analysis as analysis
from . import SentimentModel as sentiment
import json
# Create your views here.
def home_page(request):
    request.session['search']="unknown"
    search=request.session.get('search','unknown')
    print(search)
    return render(request,'index.html')


def dashboard(request,data):
    #data retrieval function
    obj=dr.DataRetrieval()
    res=obj.get_all_reviews(data)

    res = sentiment.SentimentModel.get_sentiment(res)
    sent , sent_count = sentiment.SentimentModel.count_sentiment(res)
    labels_positive, counts_positive, labels_negative, counts_negative = analysis.Analysis.line_analysis(res)
    search=request.session.get('search','unknown')
    js = res.to_json(orient = 'records' , date_format = 'iso')
    request.session['res']=js
    context={'search':search,'sent':sent , 'sent_count':sent_count,'labels_positive':labels_positive, 'counts_positive':counts_positive
    , 'labels_negative':labels_negative, 'counts_negative':counts_negative}
    # if 'search' not in request.session:
    # if search == 'unknown':
    #     print(search)
    #     return render(request,'index.html')
    return render(request,"udashboard.html",context) 
def get_data(request):
    if request.method == 'POST':
         data = request.POST['search']
         request.session['search']=data
    else:
        data=request.session.get('search','unknown')
    # obj=dr.DataRetrieval()
    # res=obj.get_all_reviews(data)
    #search=request.session.get('search','unknown')
    if not request.session['search']:
       
        return render(request,'index.html')
    else:
          
         return dashboard(request,data)
  
# redirect to tweets page   
def tweets(request):
    search=request.session.get('search','unknown')
    response=request.session.get('res','unknown')
    res = json.loads(response)
    print(type(res))
    print(search)
    
    # if search == 'unknown':
    #     return render(request,'index.html')
    # else:    
    #response=requests.get('https://api.covid19api.com/countries').json()
    # if not request.session['search']:
    #   return render(request,'index.html')
    # else:
    return render(request,'utweets.html',{'search':search,'response':res})
def success(request,data):
    return render(request,'search.html',{'data':data})

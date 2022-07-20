# Create your views here.
from django.shortcuts import render,redirect
from . models import Url, Statistic
from . forms import UrlForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from . statistics import calculate_popularity

def home(request):
    '''
    This is the homepage view function.
    It accepts both GET and POST requests from
    the Template
    '''
    print("*"*80)
    print("Home")
    # check if the user is sending a post request
    if request.method == 'POST':
        form = UrlForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            search_name = form.cleaned_data['Enter_url']
            is_exist = Url.url_exist(search_name)
            # if the url doesn't already exist in the database
            if not is_exist:
                print("doesn't exist")
                shortcode = Url.code_generator()
                new_url = Url(short_id = shortcode,httpurl = search_name )
                # save the new url to the Url table in the database
                new_url.save()
                
                # httpurl = search_name 
                # requested_object = Url.objects.get(httpurl = search_name)
                # message = 'short code created successfully'

                # # get the total number of clicks for this url from the database
                # total_clicks = Statistic.get_total_clicks()
                # simulate the total number of clicks on other urls as 5 
                # :ToDo To be changed 
                total_clicks = 5

            else:
                # return dict
                return_dict = {"message":"","shortcode":"","httpurl":"","requested_object":"",
                    "total_clicks":0
                }
                # try and except to ensure a fail safe situation
                try:
                    #filter url record with httpurl
                    found_url = Url.objects.filter(httpurl = search_name).values()[0]
                    # update the return dict values approriately
                    return_dict["shortcode"] = found_url.get("short_id")
                    return_dict["httpurl"] = found_url.get("httpurl")
                    return_dict["requested_object"] = Url.objects.get(httpurl = search_name)
                    return_dict["message"] = 'A short url for the entered url already exists'
                    # get the total number of clicks for this url from the database
                    # total_clicks = Statistic.get_total_clicks()
                    # simulate the total number of clicks on other urls as 5 
                    # :ToDo To be changed 
                    return_dict["total_clicks"] = 5
                except:
                    return_dict["message"] = 'An error occured while retriving URL'
                    # get the total number of clicks for this url from the database
                    # total_clicks = Statistic.get_total_clicks()
                    # simulate the total number of clicks on other urls as 5 
                    # :ToDo To be changed 
                    return_dict["total_clicks"] = 5

            #return the short url page with statistics
            return render(request,'makeshort.html',return_dict)

        else:
            print("Form is invalid")
    else:
        # user is sending a normal request
        form = UrlForm()
    # return the template page
    return render(request,'home.html',{"form":form})

def r(request):    
    shortcode = Url.objects.get(httpurl = search_name).short_id
    urls = Url.objects.all()
    total_clicks = Statistic.get_total_clicks()

    for url in urls:
        index = calculate_popularity(total_clicks,url.count)
        url.index = index
        url.save()
    return render(request,'makeshort.html',{"message":message,"shortcode":shortcode, "httpurl":httpurl})

def s(request, shortcode):
    try:
        is_shortcode = Url.shortcode_exist(shortcode)
        if is_shortcode == True:
            requested_url = Url.get_url_by_shorcode(shortcode)
            requested_url.count +=1
            requested_url.save()
            increase_total = Statistic.objects.get(name = 'statistics')
            increase_total.total_clicks += 1
            increase_total.save()

            total_clicks1 = Statistic.get_total_clicks()
            urls = Url.objects.all()
            for url in urls:
                index = calculate_popularity(total_clicks1,url.count)
                url.index = index
                url.save()
            return redirect(requested_url.httpurl)
        else:
            return redirect(l)
    except:
        return redirect(w)

def l(request):
    message = ''
    return render(request, 'last.html',{"message":message})

def a(request): 
    urls = Url.objects.all()
    total_clicks = Statistic.get_total_clicks()

    for url in urls:
        index = calculate_popularity(total_clicks,url.count)
        url.index = index
        url.save()
    return render(request,'all.html',{"urls":urls,"total_clicks":total_clicks,"index":index})

def w(request):
    return render(request,'wrong.html')

def t(request):
    '''
    this is a general test view function that enables me to test the various aspects 
    of the app before applying changes to an intended view function
    '''
    form = UrlForm()
    if request.method == 'POST':

        form = UrlForm(request.POST)

        if form.is_valid():
            search_name = form.cleaned_data['entered_url']
            
            return render(request,'test2.html',{"message":search_name,"form":form})
    else:
        form = UrlForm()
    return render(request,'test.html',{"form":form})

def p(request):
    length = 50
    return render(request,'p.html',{"length": length})

def i(request):
    length = 50
    return render(request,'single.html')

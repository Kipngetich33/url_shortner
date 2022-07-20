# Create your views here.
from django.shortcuts import render,redirect
from . models import Url, Statistic
from . forms import UrlForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from . statistics import calculate_popularity
from django.conf import settings
from decouple import config

def home(request):
    '''
    This is the homepage view function.
    It accepts both GET and POST requests from
    the Template
    '''
    # check if the user is sending a post request
    if request.method == 'POST':
        form = UrlForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            # initialize shortcode as empty string
            shortcode = ""
            # get the entered url
            entered_long_url = form.cleaned_data['Enter_url']
            is_exist = Url.url_exist(entered_long_url)
            # if the url doesn't already exist in the database
            if not is_exist:
                # generate a shortcode to represent the url in the database
                shortcode = Url.code_generator()
                new_url = Url(short_id = shortcode,httpurl = entered_long_url )
                # save the new url to the Url table in the database
                new_url.save()
            else:
                #filter url record with httpurl to get the related shortcode
                shortcode = Url.objects.filter(httpurl = entered_long_url).values()[0].get("short_id")                
            #return the short url page with statistics
            return redirect(url_detail_view,shortcode)

        else:
            # an error occured redirect to error page
            return redirect(error_page)
    else:
        # user is sending a normal request
        form = UrlForm()
    # return the template page
    return render(request,'home.html',{"form":form})

def url_detail_view(request,shortcode):
    '''
    This the urls details view, the function takes a url shortcode
    and retrives all infomation relating to it from the database
    input:
        shortcode - slug
    '''
    # get the base url from the enviroment variables (using python-decouple)
    base_url = config("BASE_URL", default = "http://localhost") 
    
    # define the retrun dict
    return_dict = {
        "message":"Mesage here",
        "click_through_rate":10,
        "base_url":base_url
    }

    # get url details from the model class using get_class_information
    url_details = Url.get_class_information(shortcode)
    # get statistics for url


    # check if related url was found
    if url_details.get("state"):
        return_dict['url_details'] = url_details
    else:
        # redirect to the error page
        return redirect(error_page)

    # return the view template
    return render(request,'url_details.html',return_dict)

def redirect_short_to_long_url(request,shortcode):
    '''
    Function that redirects the given short url to the 
    initial long url
    '''
    # get a url associated with shortcode
    try:
        long_url = Url.get_url_by_shorcode(shortcode)
        # redirect user to correct url
        return redirect(str(long_url))
    except:
        # no match found hence redirect to error page
        return redirect(error_page)

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

def error_page(request):
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

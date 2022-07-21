from django.db import models
import random

# Create your models here.
class Url(models.Model):
    short_id = models.SlugField(max_length=6,primary_key=True)
    httpurl = models.URLField(null = True)
    pub_date = models.DateTimeField(auto_now=True)
    count = models.PositiveIntegerField(default=0)
    index = models.IntegerField(default=0,null = True)
 
    def __str__(self):
        return self.httpurl

    @classmethod
    def count_unique(cls,httpurl):
        '''
        Method that counts the number of object with a given httpurl in the database
        '''
        all = cls.objects.filter(httpurl = httpurl).count()
        return all

    @classmethod
    def shortcode_exist(cls,short_id):
        '''
        Method that determines whether a provided short_id exists in the database
        '''
        is_exitent = cls.objects.filter(short_id = short_id).count()
        if is_exitent > 0:
            return True
        else:
            return False

    @classmethod
    def url_exist(cls,httpurl):
        '''
        Method that determines whether a provided httpurl exists in the database
        '''
        is_exitent = cls.objects.filter(httpurl = httpurl).count()
        if is_exitent > 0:
            return True
        else:
            return False

    @classmethod
    def code_generator(cls,size = 6 , char = '1234567890afuhufxrkerwcklbvds' ):
        '''
        Method that creates a unique shortcode for each given httpurl
        '''
        new_code = ''
        for i in range(size):
            new_code += random.choice(char)
        is_exitent = cls.shortcode_exist(new_code)
        if is_exitent == True:
            cls.code_generator()
        else:
            return new_code
    
    @classmethod
    def get_url_by_shorcode(cls,short_id):
        '''
        Method that fetches a url object attached to the provided short_id
        '''
        url = cls.objects.get(short_id= short_id)
        return url

    
    class Meta:
        '''
        Order urls based on the number of clicks
        '''
        ordering = ['-count']

    @classmethod
    def get_shortcode_by_url(cls,httpurl):
        '''
        Method that returns the url object based on the provided httpurl
        '''
        requested_url = cls.objects.get(httpurl = httpurl)
        return requested_url

    @classmethod
    def get_class_information(cls,shortcode):
        '''
        Function that uses the shortcode of a model and 
        uses it to get all the columns in a model
        input:
            shortcode - str
        output:
            dictionary with all the fields  
        '''
        # declare the return dictionary
        return_dict = {'count':None, 'httpurl':None, 'index':None,
            'pub_date':None, 'short_id':None,"state":False
        }
        # now get the fields and values
        fields_n_values = cls.objects.filter(short_id = shortcode).values_list('count', 'httpurl', 'index', 'pub_date', 'short_id')[0]
        if len(fields_n_values):
            # add correct values to the dictionary
            return_dict['url_clicks'] = fields_n_values[0]
            return_dict['long_url'] = fields_n_values[1]
            return_dict['index'] = fields_n_values[2]
            return_dict['pub_date'] = fields_n_values[3]
            return_dict['shortcode'] = fields_n_values[4]
            return_dict['state'] = True

        # return data formatted as a dictionary
        return return_dict

class Statistic(models.Model):
    '''
    Class that defines the structure of the statistics objects
    '''
    short_id = models.SlugField(max_length=6, default = None)
    pub_date = models.DateTimeField(auto_now=True)

    @classmethod
    def get_total_clicks(cls):
        '''
        Method that get the total number of click throughs in the
        database
        '''
        return cls.objects.count()

    @classmethod
    def get_clicks_per_url(cls,shortcode):
        '''
        Method that get the total number of click throughs for a specific
        url
        input:
            shortcode - slug
        output:
            count - int
        '''        
        return cls.objects.filter(short_id = shortcode).count()

    @classmethod
    def get_url_stats(cls,shortcode):
        '''
        Function that gets all stats related to a given url shortcode
        input:
            shortcode
        output:
            stats_dict - dictionary with stats
        '''
        # initialize the stats dictionary as empty
        stats_dict = {}
        # add total clicks and total clicks per url count
        stats_dict['total_clicks'] = cls.get_total_clicks()
        stats_dict['clicks_per_url'] = cls.get_clicks_per_url(shortcode)
        try:
            stats_dict['share_percentage'] = stats_dict['clicks_per_url'] / stats_dict['total_clicks'] * 100
        except:
            stats_dict['share_percentage'] = 0

        # return the stats dictionary
        return stats_dict

    def calculate_popularity(url_clicks):
        '''
        Method that calculates the popularity of a particular based on the number of clicks and 
        total number of clicks on the app
        '''
        pass

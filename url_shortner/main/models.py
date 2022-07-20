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

    def save_url(self):
        '''
        Method that saves Urls objects
        '''
        print("saving url")
        # save a corresponding Statistic record
        new_statistic = Statistic(name = self.short_id,total_clicks = 0 )
        new_statistic.save()
        

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
        print("*"*80)
        print("dict values")
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
    name =  models.CharField(max_length = 30, default ='statistics')
    total_clicks = models.PositiveIntegerField(default=1)

    @classmethod
    def get_total_clicks(cls):
        print("*"*80)
        print("getting ttoal clicks")
        total = cls.objects.get(name = 'statistics')
        return total.total_clicks

    def calculate_popularity(url_clicks):
        '''
        Method that calculates the popularity of a particular based on the number of clicks and 
        total number of clicks on the app
        '''
        pass
## quotes/views.py
##view func handler/wrapper funcs + storage of images and quotes go here
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time
IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/JunaidJamshed-YeWatanShoot_%28cropped%29.jpg/1200px-JunaidJamshed-YeWatanShoot_%28cropped%29.jpg",
    "https://m.economictimes.com/thumb/msid-55857629,width-1200,height-900,resizemode-4,imgsize-41618/singer-turned-preacher-junaid-jamshed-feared-dead-in-pak-crash.jpg",
    "https://i.tribune.com.pk/media/images/49469-jjmainjpg-1494316262/49469-jjmainjpg-1494316262.jpg",
    "https://img.dunyanews.tv/news/2024/December/12-08-24/news_big_images/855288_84519627.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuqC1JceFBNHLQuNhs86H7x_mr7js-GH_SSQ&s",
]
QUOTES = [
    "Dil Dil Pakistan, Jaan Jaan Pakistan.",  
    "When you want something, all the universe conspires in helping you to achieve it.",  
    "Success is not in what you have, but who you are.",  
    "Life is temporary; prepare for the eternal life in the Hereafter.",  
    "Music was my passion, but faith gave my life a new direction.",  
    "Happiness is found in simplicity and gratitude.",  
    "When you choose to serve others, you find true contentment.",  
    "The real success is not in fame or fortune, but in inner peace and faith."]

def about(request):
    '''
    render handle passer for the about page
    '''
    template_name = 'quotes/about.html'

    context = {
        "current_time" : time.ctime()
    }
    return render(request, template_name, context)
def quote(request):
    '''
    same as above, handle passing the rendering but for quote page
    '''
    template_name = 'quotes/quote.html'
    quote = random.choice(QUOTES)
    image = random.choice(IMAGES)

    context = {
        'current_time' : time.ctime(),
        'quote': quote,
        'image': image
    }
    return render(request, template_name, context)

def show_all(request):
    '''
    same as above but for show_all page
    '''
    template_name = 'quotes/show_all.html'
    context = {
        "current_time" : time.ctime(),
        'quotes': QUOTES,
        'images': IMAGES
    }
    return render(request, template_name, context)
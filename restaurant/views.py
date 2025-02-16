from django.shortcuts import render, redirect
import time
import random
from datetime import datetime, timedelta

MEALS = [
    "Secret ingredient mix",
    "Ultra deluxe topping",
    "Mystery platter",
    "Limited edition soda",
    "Celebrity signature meal",
]

def home(request):
    template_name = "restaurant/main.html"
    data = {"timestamp": time.ctime()}
    return render(request, template_name, data)

def menu(request):
    template_name = "restaurant/order.html"
    data = {"timestamp": time.ctime(), "special": random.choice(MEALS)}
    return render(request, template_name, data)

def receipt(request):
    template_name = "restaurant/confirmation.html"
    
    if request.POST:
        items_cost = {
            'grilled_plate': 9,
            'beef_platter': 11,
            'seafood_special': 12,
            'snack_pack': 4,
            'beverage': 2,
        }

        specials_cost = {
            "Secret ingredient mix": 2,
            "Ultra deluxe topping": 3,
            "Mystery platter": 14,
            "Limited edition soda": 3,
            "Celebrity signature meal": 7,
        }

        selected_items = []
        total = 0

        for item, cost in items_cost.items():
            if item in request.POST:
                selected_items.append(f"{item.replace('_', ' ').title()} - ${cost}")
                total += cost

        if 'special' in request.POST:
            special_name = request.POST['special']
            special_cost = specials_cost.get(special_name, 6)
            selected_items.append(f"{special_name} - ${special_cost}")
            total += special_cost

        notes = request.POST.get('notes', '')
        client_name = request.POST.get('client_name', '')
        contact = request.POST.get('contact', '')
        email_address = request.POST.get('email_address', '')

        pickup_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        data = {
            "timestamp": time.ctime(),
            "selected_items": selected_items,
            "total": total,
            "notes": notes,
            "client_name": client_name,
            "contact": contact,
            "email_address": email_address,
            "pickup_time": pickup_time,
        }

        return render(request, template_name, data)
    
    return redirect("menu")

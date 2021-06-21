from hospital.models import Donor
import random
import re
import os
import json
from pprint import pprint


def get_city_choices():
    
    from misc.models import City
    city_list = [(str(city.id), city.name) for city in City.objects.all()]
    city_list.insert(0, ('---', 'Select your city'))
    return tuple(city_list)
    return (('a', 'a'), ('b', 'b'))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

    
def beautify_username(func):
    '''Decorator function to make the username from full name.'''
    def beautify(username):
        username = username.split(' ')[0].lower()
        username = username.replace('.', '')
        username = username.replace('-', '')
        return func(username)
    return beautify


def get_random_string(size=1):
    '''Generates random string of size `size`'''
    return ''.join(random.choice('0123456789') for _ in range(size))


@beautify_username
def generate_unique_username(username):
    '''Generates a username from a given string.'''

    if len(username) < 3:
        username = username + get_random_string(size=1)
        return generate_unique_username(username)

    if Donor.objects.filter(username=username).exists():
        return generate_unique_username(username + get_random_string(size=1))
    return username


def valid_name(name):
    if re.compile("[a-z -._A-Z]+$").match(name):
        return True
    return False


def valid_phone(phone, exist_check=True):
    # Length check
    if len(phone) != 11:
        return False
    # 01xxxxxxxxx format check
    if phone[0] != '0' or phone[1] != '1':
        return False
    if exist_check:
        if Donor.objects.filter(phone=phone).exists():
            return False
    if not re.compile("^[0-9]+$").match(phone):
        return False
    return True

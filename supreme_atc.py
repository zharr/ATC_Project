import requests, json, random, time, threading

base_url = 'http://www.supremenewyork.com'

# Classes to be used
class Products(object):
    def __init__(self, category, keywords, colors, sizes, quantity):
        self.category = category
        self.keywords = keywords
        self.colors = colors
        self.sizes = sizes
        self.quantity = quantity
        self.in_cart = False
        self.id = None

class Task(object):
    def __init__(self, products, interval=1, ghost=1, proxies={}):
        self.id = random.getrandbits(128)
        self.active = False
        self.parent = None
        self.products = products
        self.interval = interval
        self.ghost = ghost
        self.sesion = requests.session()
        self.sesion.proxies.update(proxies)

    def toggle(self):
        self.active = not self.active

class Card(object):
    def __init__(self, cardtype, number, month, year, cvv):
        self.cardtype = cardtype
        self.number = number
        self.month = month
        self.year = year
        self.cvv = cvv

class Address(object):
    def __init__(self, address_1, address_2, zipcode, city, state, country='USA'):
        self.address_1 = address_1
        self.address_2 = address_2
        self.zipcode = zipcode
        self.city = city
        self.country = country

class Account(object):
    def __init__(self, first_name, last_name, email, tel, address, card, tasks=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.tel = tel
        self.address = address
        self.card = card
        self.tasks = tasks

    def register_task(self, task):
        if task.parent is not None:
            task.parent.remove_task(task)
        task.parent = self
        self.tasks.append(task)

    def remove_task(self, task):
        task.parent = None
        self.tasks.remove(task)

    def stop_all_tasks(self):
        for task in (tasks for tasks in self.task if tasks.active):
            task.toggle

    def start_all_tasks(self):
        for task in (tasks for tasks in self.tasks if not tasks.active):
            task.toggle
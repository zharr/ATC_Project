import requests, json, random, time, threading, datetime
import timeit
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs


ua = UserAgent()
headers = {'User-Agent' : str(ua.random)}
base_url = 'https://kith.com/'
shop_url = 'https://shop.kithnyc.com'
keywords = ['stance', 'classics', 'crew', 'white']
size = 'OS'
email = 'zach.harrison55@gmail.com'
shipping_address = '15407 Elm Rd N'
shipping_city = 'Maple Grove'
shipping_country = 'US'
first_name = 'Zach'
last_name = 'Harrison'
phone_number = '7635673484'
shipping_state = 'Minnesota'
shipping_zip = '55311'
card_number = '0000000000000000'
card_exp_month = '11'
card_cvv = '965'
card_exp_year = '2020'

def log(event):
    print(str(datetime.datetime.now().strftime('%H:%M:%S')) + ' ::: ' + str(event))

def tick():
    global tick
    tick = timeit.default_timer()
    return tick

def tock():
    tock = timeit.default_timer()
    print(tock - tick)
    return tock

def main():
    session = requests.Session()

    # get page from requests
    r = session.get(base_url+"/collections/accessories/mens", headers=headers)

    # parse with beautiful soup
    soup = bs(r.text, "lxml")
    product = ""
    found = False
    # omptimize this...
    print('Looking for product...')
    for link in soup.find_all('a'):
        for s in keywords:
            if s not in link.get('href'):
                found = False
                break
            else:
                product = link.get('href')
                found = True
        if found:
            print('Product found.')
            break



    # add to cart
    r = session.get(base_url + product, headers=headers)
    soup = bs(r.text, "lxml")
    form = soup.find('form', {'id' : 'AddToCartForm'})


    size_select = soup.find('select', {'id' : 'productSelect'})

    for cur_size in size_select.find_all('option'):
        if cur_size.text == size:
            print("Size " + size + " available.")
            id = cur_size['value']
            break

    payload = {
            'id': id,
            'quantity': '1'
    }
    time.sleep(2)
    r = session.post(base_url + '/cart/add.js', data=payload, headers=headers)

    # navigate to cart
    time.sleep(2)
    r = session.get(base_url + '/cart', headers=headers)

    # navigate to checkout (need to pass token and utf character i think)
    print('Checking out...')
    time.sleep(2)
    r = session.get(base_url + '/checkout', headers=headers)

    soup = bs(r.text, 'lxml')
    form = soup.find('form', {'class' : 'edit_checkout'})
    time.sleep(2)
    payload = {
            'utf8': '✓',
            '_method': 'patch',
            'button': '',
            'authenticity_token': form.find('input', {'name' : 'authenticity_token'})['value'],
            'previous_step': 'contact_information',
            'checkout[email]': email,
            'checkout[shipping_address][first_name]': first_name,
            'checkout[shipping_address][last_name]': last_name,
            'checkout[shipping_address][address1]': shipping_address,
            'checkout[shipping_address][address2]': '',
            'checkout[shipping_address][city]': shipping_city,
            'checkout[shipping_address][country]': shipping_country,
            'checkout[shipping_address][province]': '',
            'checkout[shipping_address][province]': '',
            'checkout[shipping_address][province]': shipping_state,
            # 'checkout[shipping_address][province]': ',,' + shipping_state,
            'checkout[shipping_address][zip]': shipping_zip,
            'checkout[shipping_address][phone]': phone_number,
            'remember_me': 'false',
            'checkout[client_details][browser_height]': '728',
            'checkout[client_details][browser_width]': '1280',
            'checkout[client_details][javascript_enabled]': '0',
            'step': 'shipping_method',
    }

    time.sleep(2)
    r = session.post(shop_url + form['action'], data=payload, headers=headers)

    soup = bs(r.text, 'lxml')
    form = soup.find('form', {'class' : 'edit_checkout'})

    payload = {
            '_method': 'patch',
            'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
            'button': '',
            'checkout[client_details][browser_height]': '728',
            'checkout[client_details][browser_width]': '1280',
            'checkout[client_details][javascript_enabled]': '0',
            'checkout[shipping_rate][id]': 'shopify-UPS%20GROUND%20(5-7%20business%20days)-10.00',
            'previous_step': 'shipping_method',
            'step': 'payment_method',
            'utf8': '✓'
    }

    time.sleep(2)
    r = session.post(shop_url + form['action'], data=payload, headers=headers)

    # r = session.get(shop_url + form['action'] + '?step=payment_method', headers=headers)

    soup = bs(r.text, 'lxml')
    form = soup.find_all('form', {'class': 'edit_checkout'})[-1]

    payload = {
        'utf8': '✓',
        '_method': 'patch',
            'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
            #'c': form.find('input', {'name': 'c'})['value'],
            #'d': form.find('input', {'name': 'd'})['value'],
            'checkout[buyer_accepts_marketing]': '0',
            'checkout[client_details][browser_height]': '728',
            'checkout[client_details][browser_width]': '1280',
            'checkout[client_details][javascript_enabled]': '1',
            'checkout[credit_card][expiry_month]': card_exp_month,
            'checkout[credit_card][name]': first_name + ' ' + last_name,
            'checkout[credit_card][number]': card_number,
            'checkout[credit_card][verification_value]': card_cvv,
        # try getting rid of checkou[credit_card]
            'checkout[credit_card][year]': card_exp_year,
            'checkout[credit_card][vault]': 'false',
            'checkout[different_billing_address]': 'false',
            'checkout[payment_gateway]': form.find('input', {'name': 'checkout[payment_gateway]'})['value'],
            'complete': '1',
            'expiry': card_exp_month + '/' + card_exp_year[-2:],
            'previous_step': 'payment_method',
            's': '',
            'step': '',
    }

    time.sleep(2)
    response = session.post(shop_url + form['action'], data=payload, headers=headers)
    # print(r.text)
    print(response.status_code)
    print(response.url)
    print(response.text)
    soup = bs(response.text, 'lxml')
    print('header: ' +str(soup.h2))
    with open('bs4.html', 'w') as f:
        for line in soup.prettify():
            f.write(str(line))

if __name__ == '__main__':
    tick()
    main()
    tock()

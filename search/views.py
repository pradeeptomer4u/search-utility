import json
import time

from django.http import JsonResponse
from django.shortcuts import render
import requests
# Create your views here.
from django.views.generic import ListView

from search.models import Products
from threading import Thread




def shopclues_search(product):
    params = {
        'q':product,
        'key':'d12121c70dda5edfgd1df6633fdb36c0',
        'z': 1
    }
    req = requests.get("http://api.shopclues.com/api/v11/search",params=params)
    if req.status_code == 200:
        data = json.loads(req.content)
        data = data['products']
        return data

def tata_search(product):
    params = {
        'searchString':'Shorts',
        'type':'category',
        'channel':'mobile',
        'pageSize':20,
        'typeID':'al',
        'page':0,
        'searchText':product,
        'isFilter':'false',
        'isTextSearch':'true'
    }
    header ={"Content-Type": "application/x-www-form-urlencoded"}
    req = requests.post("https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/serpsearch",data=params,headers=header)
    if req.status_code == 200:
        data = json.loads(req.content)
        data = data['searchresult']
        return data

def paytm_search(product):
    params = {
        'userQuery':product,
        'items_per_page':'100',
    }
    req = requests.get("https://search.paytm.com/v2/search",params=params)
    if req.status_code == 200:
        data = json.loads(req.content)
        filters = data['filters']
        data = data['grid_layout']
        data.append({'category':filters[0]['values']})
        return data

def store_in_local(product_list):
    for datas in product_list:
        if 'shopclues_search' in datas.keys():
            for data in datas['shopclues_search']:
                prod = Products.objects.filter(product_id=data['product_id'], vendor='S').count()
                if prod > 0:
                    Products.objects.filter(product_id=data['product_id'], vendor='S').update(product_name=data['product'],
                                                                                              catagory_name=data['category'],
                                                                                              catagory_id=data['category_id'],
                                                                                              price=data['price'],
                                                                                              product_url=data['product_url'],
                                                                                              image_url=data['image_url'],
                                                                                              instock=True)
                else:
                    Products.objects.create(product_id=data['product_id'], product_name=data['product'],
                                            catagory_name=data['category'], catagory_id=data['category_id'], vendor='S',
                                            price=data['price'], product_url=data['product_url'], image_url=data['image_url'],
                                            instock=True)
        category= []
        category_name = ''
        if 'paytm_search' in datas.keys():
            for data in datas['paytm_search']:
                if 'category' in data.keys():
                    category = data['category']
                    print(category)
            for data in datas['paytm_search']:
                if 'product_id' in data.keys():
                    for cat in category:
                        if int(data['category_id']) == int(cat['id']):
                            category_name = data['name']
                    prod = Products.objects.filter(product_id=data['product_id'], vendor='P').count()
                    if prod > 0:
                        Products.objects.filter(product_id=data['product_id'], vendor='P').update(product_name=data['name'],
                                                                                                  catagory_name=category_name,
                                                                                                  catagory_id=data['category_id'],
                                                                                                  price=data['offer_price'],
                                                                                                  product_url=data['url'],
                                                                                                  image_url=data['image_url'],
                                                                                                  instock=True)
                    else:
                        Products.objects.create(product_id=data['product_id'], product_name=data['name'],
                                                catagory_name=category_name, catagory_id=data['category_id'], vendor='P',
                                                price=data['offer_price'], product_url=data['url'], image_url=data['image_url'],
                                                instock=True)
        if 'tata_search' in datas.keys():
            for data in datas['tata_search']:
                prod = Products.objects.filter(product_id=data['productId'], vendor='T').count()
                if prod > 0:
                    Products.objects.filter(product_id=data['productId'], vendor='T').update(product_name=data['productname'],
                                                                                              catagory_name=data['productCategoryType'],
                                                                                              catagory_id=data['ussid'],
                                                                                              price=data['sellingPrice']['value'],
                                                                                              product_url=data["galleryImagesList"][0]["galleryImages"][1]["value"],
                                                                                              image_url=data['imageURL'],
                                                                                              instock=True)
                else:
                    Products.objects.create(product_id=data['productId'], product_name=data['productname'],
                                            catagory_name=data['productCategoryType'], catagory_id=data['ussid'], vendor='T',
                                            price=data['sellingPrice']['value'], product_url=data["galleryImagesList"][0]["galleryImages"][1]["value"], image_url=data['imageURL'],
                                            instock=True)

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

class ListRCEntryView(ListView):
    template_name = 'search/products_home.html'
    paginate_by = 50
    ordering = 'id'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        product_list = []
        product = self.request.GET.get('product',None)
        if product:
            twrv = ThreadWithReturnValue(target=shopclues_search, args=(product,))
            twrv.start()
            print('shopclues_search')
            product_list.append({'shopclues_search':twrv.join()})
            twrv = ThreadWithReturnValue(target=tata_search, args=(product,))
            twrv.start()
            print('tata_search')
            product_list.append({'tata_search':twrv.join()})
            twrv = ThreadWithReturnValue(target=paytm_search, args=(product,))
            twrv.start()
            product_list.append({'paytm_search':twrv.join()})
            twrv = Thread(target=store_in_local, args=(product_list,))
            twrv.daemon= True
            twrv.start()
            print('store_in_local')
            prod_list = product.split(' ')
            print(len(prod_list))
            if len(prod_list) > 1:
                for product in prod_list[::-1]:
                    prodct = Products.objects.filter(product_name__iexact=product)
                    if prodct.count() > 0:
                        queryset = prodct
                        print('exact')
                    else:
                        prodct = Products.objects.filter(product_name__istartswith=product)
                        if prodct.count() > 0:
                            queryset = prodct
                            print('startwith')
                        else:
                            prodct = Products.objects.filter(product_name__icontains=product)
                            queryset = prodct
                            print('contain')
            else:
                prodct = Products.objects.filter(product_name__iexact=product)
                if prodct.count() > 0:
                    queryset  = prodct

                else:
                    prodct = Products.objects.filter(product_name__istartswith=product)
                    if prodct.count() > 0:
                        queryset = prodct

                    else:
                        prodct = Products.objects.filter(product_name__icontains=product)
                        queryset = prodct

        else:
            queryset = Products.objects.all()[:10]
        return queryset

    def get_context_data(self, **kwargs):
        prodc = self.request.GET.get('product',None)
        context = super(ListRCEntryView, self).get_context_data(**kwargs)
        if prodc:
            context['product'] = prodc

        return context
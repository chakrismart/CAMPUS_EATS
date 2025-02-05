from home.models import Product
class Cart():

    def __init__(self,request):

        self.session=request.session

        cart=self.session.get('session_key')

        if 'session_key' not in request.session:

            cart=self.session['session_key']={}
        self.cart=cart
        
    def add(self,product,quantity):
        product_id=str(product.id)
        product_quantity=str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=int(product_quantity) #ikkada str() ivvali endukante django stores session data as json.json doesnt support decimal data
            #price is decimal field

        self.session.modified=True

    def get_products(self):

        product_ids=self.cart.keys()

        products=Product.objects.filter(id__in=product_ids)
        return products


    def get_quantities(self):

        quants=self.cart
        #print(quants)
        return quants  

    def update(self,product_id,product_quantity):
        ourcart=self.cart
        product_id=str(product_id)
        ourcart[product_id] = product_quantity
        self.session.modified = True  

    def delete(self,product_id):
        
        product_id=str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True 

    def get_total(self):
        quantities=self.cart
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        total=0
        # print('hi')
        # print(quantities)
        for key,value in quantities.items():
            key=int(key)
            for product in products:
                if key==product.id:
                    #print(type(product.price),type(value))
                    total=total+(int(value)*product.price)
        return total
        




         
from services.cart import add_to_cart

def addcart(request, category, stockcode):
    if request.method == 'GET':
        quantity = int(request.GET['quantity'])
        add_to_cart(stockcode, category, quantity)
    return render(request, 'deltago/index.html')
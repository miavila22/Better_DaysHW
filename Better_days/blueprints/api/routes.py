from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from Better_days.models import Customer, Product, ProdOrder, Order, db, product_schema, products_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/token', methods = ['GET', 'POST'])
def token():
    
    data = request.json

    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client Id. Try Again!' 

        }
    
@api.route('/shop')
@jwt_required()
def get_shop():

    allprods = Product.query.all()

    response = products_schema.dump(allprods) 
    return jsonify(response)

@api.route('/order/create/<cust_id>', methods = ['POST']) 
@jwt_required()
def create_order(cust_id):

    data =  request.json

    customer_order = data['order']  
    print("customer_order", customer_order)

    customer = Customer.query.filter(Customer.cust_id == cust_id).first() 
    if not customer: 
        customer = Customer(cust_id)
        db.session.add(customer)

    order = Order()
    db.session.add(order)

    for product in customer_order:


        prodorder = ProdOrder(product['prod_id'], product['qty'], product['price'], order.order_id, customer.cust_id )
        db.session.add(prodorder)

        order.increment_ordertotal(prodorder.price)

        current_product = Product.query.get(product['prod_id'])
        
        current_product.decrement_quantity(product['qty'])

    db.session.commit()

    return {
        'status' : 200,
        'message' : 'New Order was Created.'
    }

@api.route('/order/<cust_id>')
@jwt_required()
def get_orders(cust_id):

    #need to grab all prodorders associated with that customer
    prodorder = ProdOrder.query.filter(ProdOrder.cust_id == cust_id).all()

    data= []
    for order in prodorder:

        product = Product.query.filter(Product.prod_id == order.prod_id).first()

        product_dict = product_schema.dump(product)

        product_dict['qty'] = order.qty
        product_dict['order_id'] = order.order_id
        product_dict['id'] = order.prodorder_id

        data.append(product_dict)

    return jsonify(data)

@api.route('/order/update/<order_id>', methods = ['PUT']) #whenever we are updating we using PUT
@jwt_required()
def update_order(order_id):

    data = request.json
    new_qty = int(data['qty'])
    prod_id = data['prod_id']



    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)



    prodorder.set_price(product.price, new_qty)


    diff = abs(new_qty - prodorder.quantity)


    if prodorder.quantity > new_qty: 
        product.increment_quantity(diff) #we are putting some products back
        order.decrement_ordertotal(prodorder.price) #our order total is less $ now 

    elif prodorder.quantity < new_qty:
        product.decrement_quantity(diff) #we are taking more quantity aaway
        order.increment_ordertotal(prodorder.price) #our order total is more $ now 

    prodorder.update_quantity(new_qty)

    db.session.commit()

    return {
        'status': 200,
        'messagae': 'Order was Updated Successfully'
    }
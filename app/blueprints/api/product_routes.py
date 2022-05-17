from . import bp as api
from app.models import *
from flask import make_response, request, abort
from app.blueprints.auth.authy import token_auth
from helpers import require_admin


@api.get('/product')
def get_products():
    products = Product.query.all()
    products = [product.to_dict() for product in products]
    return make_response({"product":products},200)

@api.get('/product/<int:id>')
def get_product(id):
    p = Product.query.get(id)
    if not p:
        abort(404)
    return make_response(p.to_dict(), 200)

@api.get('/product/type/<int:id>')
def get_products_by_type(id):
    type =Type.query.get(id)
    if not type:
        abort(404)
    all_products_in_type = [product.to_dict() for product in type.products]
    return make_response({"products":all_products_in_type}, 200)

@api.post('/product')
@token_auth.login_required()
@require_admin
def create_product():
    product_data = request.get_json() #this retrieves the payload/body
    product = Product(**product_data)
    product.save()
    type =Type.query.get(product.type_id)
    type.products.append(product)
    type.save()
    return make_response(f'Product id: {product.id} created', 200)

@api.put('/product/<int:id>')
@token_auth.login_required()
@require_admin
def put_product(id):
    put_data = request.get_json()
    product = Product.query.get(id)
    if not product:
        abort(404)
    
    temp ={}
    p = product.to_dict()
    for cat in ['name','desc','price','image','type_id']:
        if put_data.get(cat):
            temp[cat] = put_data[cat]
        else:
            temp[cat] = p[cat]
            
   
    product.from_dict(temp)
    product.save()
    return make_response(f'Product ID: {product.id} has been changed',200)

@api.delete('/product/<int:id>')
@token_auth.login_required()
@require_admin
def del_product(id):
    product = Product.query.get(id)
    if not product:
        abort(404)
    type =Type.query.get(product.type_id)
    type.products.remove(product)
    product.delete()
    return make_response(f'Product ID: {id} has been deleted',200)
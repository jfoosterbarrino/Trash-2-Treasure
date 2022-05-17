from . import bp as api
from app.models import *
from flask import make_response, request, abort
from app.blueprints.auth.authy import token_auth
from helpers import require_admin


@api.get('/type')
def get_types():
    types = Type.query.all()
    types_dicts = [type.to_dict() for type in types]
    return make_response({"types":types_dicts},200)

@api.get('/type/<int:id>')
def get_type(id):
    t = Type.query.get(id)
    if not t:
        abort(404)
    return make_response(t.to_dict(), 200)

# create new type
# {
#     "name":"my type name"
# }

@api.post('/type')
@token_auth.login_required()
@require_admin
def post_type():
    type_name = request.get_json().get("name") #this retrieves the payload/body
    type = Type(name =type_name)
    type.save()
    return make_response(f'Type  id: {type.id} with name {type.name} created', 200)

@api.put('/type/<int:id>')
@token_auth.login_required()
@require_admin
def put_type(id):
    put_data = request.get_json()
    type = Type.query.get(id)
    if not type:
        abort(404)
    type.edit(put_data['name'])
    type.save()
    return make_response(f'Type ID: {type.id} has been changed',200)

@api.delete('/type/<int:id>')
@token_auth.login_required()
@require_admin
def del_type(id):
    type = Type.query.get(id)
    if not type:
        abort(404)
    type.delete()
    return make_response(f'Type ID: {id} has been deleted',200)
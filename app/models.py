from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique = True, index =True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    products = db.relationship('Product',
                    cascade = "all, delete",
                    secondary = "cart",
                    backref = "user",
                    lazy = 'dynamic'
                    )
    icon = db.Column(db.String)

    def __repr__(self):
        return f'<Customer: {self.email} | {self.id}>'

    def __str__(self):
        return f'<Customer: {self.email} | {self.first_name} | {self.last_name}>'

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_hashed_password(self, password):
        return check_password_hash(self.password, password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/initials/{self.first_name[0]}{self.last_name[0]}.svg'

    def add_to_cart(self, item):
        self.products.append(item)
        db.session.commit()

    def del_from_cart(self, item):
        self.products.remove(item)
        db.session.commit()



@login.user_loader
def load_user(user_id):
    return Customer.get(user_id)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    desc = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    type_id = db.Column(db.ForeignKey('type.type_id'))

    def __repr__(self):
        return f'<Item: {self.product_id}|{self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.product_id,
            'name' : self.name,
            'desc' : self.desc,
            'price' :self.price,
            'image' : self.image,
            'created_on' : self.created_on,
            'type_id' : self.type_id
        }

    def from_dict(self, data):
        for field in ['name','desc','price','img','category_id']:
            if field in data:
                # object, attribute, value
                setattr(self, field, data[field])

class Type(db.Model):
    type_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    products = db.relationship('Product',
                    cascade = "all, delete-orphan",
                    backref = "type",
                    lazy = 'dynamic'
                    )

    def __repr__(self):
        return f'<Category: {self.type_id}|{self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def edit(self, new_name):
        self.name=new_name

    def to_dict(self):
        return {
            "id": self.type_id,
            "name": self.name
        }

class Cart(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key = True)

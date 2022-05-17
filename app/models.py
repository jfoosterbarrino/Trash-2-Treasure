from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class Cart(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key = True)
    
    

class Customer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique = True, index =True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    is_admin = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, index = True, unique = True)
    token_exp = db.Column(db.DateTime)
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

    def to_dict(self):
        return{
            "id": self.id,
            'first_name':self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_on': self.created_on,
            'is_admin':self.is_admin,
            'token':self.token
        }
        

    def save(self):
        db.session.add(self)
        db.session.commit()


    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        # give the user their back token if their is still valid
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        # if the token DNE or is exp
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=61)
    
    @staticmethod
    def check_token(token):
        u  = Customer.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u
    
    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/initials/{self.first_name[0]}{self.last_name[0]}.svg'

    def add_to_cart(self, item):
        self.products.append(item)
        db.session.commit()

    def del_from_cart(self, item):
        self.products.remove(item)
        db.session.commit()

    def total_cart(self):
        products = self.products.all()
        total = 0
        for product in products:
            total += product.price
        return round(total,2)

    def pay(self):
        products = self.products.all()
        for product in products:
            self.del_from_cart(product)
            



@login.user_loader
def load_user(id):
    return Customer.query.get(id)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    desc = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    type_id = db.Column(db.ForeignKey('type.id'))

    def __repr__(self):
        return f'<Item: {self.id}|{self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'desc' : self.desc,
            'price' :self.price,
            'image' : self.image,
            'created_on' : self.created_on,
            'type_id' : self.type_id
        }

    def from_dict(self, data):
        for field in ['name','desc','price','image','type_id']:
            if field in data:
                # object, attribute, value
                setattr(self, field, data[field])



class Type(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    products = db.relationship('Product',
                    cascade = "all, delete-orphan",
                    backref = "type",
                    lazy = 'dynamic'
                    )

    def __repr__(self):
        return f'<Category: {self.id}|{self.name}>'

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
            "id": self.id,
            "name": self.name
        }





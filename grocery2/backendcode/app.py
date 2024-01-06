from io import StringIO
from flask_jwt_extended import verify_jwt_in_request
from sqlalchemy import or_, and_, func
from flask import Blueprint, request, Response, make_response
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify, current_app, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from celery_config import celery
import pickle
import redis
from functools import wraps
from flask_caching import Cache


app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})
CORS(app, origins='*')
app.config['JWT_SECRET_KEY'] = 'grocery_mac'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
celery.conf.update(app.config)

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String())
    secret_key = db.Column(db.String(100))
    approved = db.Column(db.Boolean)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return f"Categories(id={self.id}, name='{self.name}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(
        'Categories', backref=db.backref('products', lazy=True))
    expiry_date = db.Column(db.Date)
    manufacture_date = db.Column(db.Date)
    price = db.Column(db.Float)
    unit = db.Column(db.String())
    quantity = db.Column(db.Float)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    created_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sold_quantity = db.Column(db.Float)

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', category_id={self.category_id}, expiry_date={self.expiry_date}, manufacture_date={self.manufacture_date}, price={self.price}),unit={self.unit},quantity={self.quantity},created_at={self.created_at}"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Float)
    total = db.Column(db.Float)
    status = db.Column(db.String)
    product_name = db.Column(db.String(100))
    product_price = db.Column(db.Float)
    buy_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    options = db.Column(db.String(255))
    category = db.Column(db.String(255))
    modification = db.Column(db.String(255))
    generated_user_id = db.Column(db.String(255))


db.create_all()


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    confirm_password = data.get('confirmPassword')
    if password != confirm_password:
        return jsonify({'message': 'Passwords do not match'}), 400

    user = User(name=name, email=email, username=username, approved=True,
                password=generate_password_hash(password), role='user')
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(
        identity=user.id, expires_delta=timedelta(days=1))
    user_info = {
        'user_id': user.id,
        'username': user.username,
        'name': user.name,
        'role': user.role,
    }

    return jsonify({'access_token': access_token, 'user': user_info}), 200


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({'message': 'Logged out successfully'})
    unset_jwt_cookies(resp)
    return resp, 200


@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Categories.query.options(joinedload('products')).all()
        categories_data = [
            {
                'id': category.id,
                'name': category.name,
                'products': [
                    {
                        'id': product.id,
                        'name': product.name,
                        'expiry_date': product.expiry_date.strftime('%Y-%m-%d'),
                        'manufacture_date': product.manufacture_date.strftime('%Y-%m-%d'),
                        'price': product.price,
                        'unit': product.unit,
                        'quantity': product.quantity,
                        'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    for product in category.products
                ],
            }
            for category in categories
        ]
        return jsonify(categories_data), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching categories.', 'error': str(e)}), 500


@app.route('/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        user_id = get_jwt_identity()
        cart_items = request.get_json()

        if not cart_items or not isinstance(cart_items, list):
            return jsonify({'message': 'Invalid request data. Please provide a list of cart items.'}), 400

        invalid_product_ids = []

        for cart_item in cart_items:
            product_id = cart_item.get('product_id')
            quantity = cart_item.get('quantity')

            if not product_id or not quantity:
                return jsonify({'message': 'Invalid cart item. Please provide product ID and quantity.'}), 400

            product = Product.query.get(product_id)

            if not product or quantity > product.quantity:
                invalid_product_ids.append(product_id)
                continue

            existing_order = Order.query.filter_by(
                user_id=user_id, product_id=product_id, status='NC').first()

            if existing_order:
                existing_order.quantity += quantity
                existing_order.total = existing_order.quantity * product.price

            else:
                total_price = quantity * product.price
                order = Order(
                    user_id=user_id,
                    product_id=product_id,
                    quantity=quantity,
                    total=total_price,
                    status='NC',
                    product_name=product.name,
                    product_price=product.price
                )
                db.session.add(order)

            product.quantity -= quantity

        db.session.commit()

        if invalid_product_ids:
            return jsonify({'message': 'Some products were not added to the cart due to insufficient quantity.', 'invalid_product_ids': invalid_product_ids}), 400

        return jsonify({'message': 'Selected products added to cart successfully!'}), 200

    except Exception as e:
        current_app.logger.error(f'Error adding products to cart: {str(e)}')
        return jsonify({'message': 'Failed to add products to cart. Please try again.'}), 500


def serialize_order(order):
    return {
        'user_id': order.user_id,
        'product_id': order.product_id,
        'quantity': order.quantity,
        'product_price': order.product_price,
        'total': order.total,
        'status': order.status,
    }


def serialize_orders(orders):
    return [serialize_order(order) for order in orders]


def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
        'unit': product.unit,
    }


@app.route('/api/<int:user_id>/order', methods=['GET'])
def get_cart_details(user_id):
    status = request.args.get('status')
    if status == 'NC':

        orders = Order.query.filter_by(user_id=user_id, status='NC').all()
    elif status == 'Purchased':
        orders = Order.query.filter_by(
            user_id=user_id, status='Purchased').all()
    else:
        return jsonify(error='Invalid status parameter. Use "NC" or "Purchased".'), 400
    total_price = 0
    orders_data = []
    for order in orders:
        product_id = order.product_id
        quantity = order.quantity
        product = Product.query.filter_by(id=product_id).first()
        subtotal = quantity * order.product_price
        total_price += subtotal
        order_data = {
            'id': order.id,
            'user_id': order.user_id,
            'product_id': order.product_id,
            'quantity': order.quantity,
            'product_price': order.product_price,
            'subtotal': subtotal,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': product.quantity,
                'unit': product.unit,
            }
        }
        orders_data.append(order_data)

    return jsonify({
        'total_price': total_price,
        'orders': orders_data
    })


@app.route('/api/customer/<int:user_id>/cart', methods=['POST'])
def cart(user_id):
    if request.method == 'POST':
        data = request.get_json()

        if 'remove' in data:
            order_id = int(data['remove'])
            order = Order.query.filter_by(id=order_id, user_id=user_id).first()
            if order:
                product_id = order.product_id
                product = Product.query.filter_by(id=product_id).first()
                if product:
                    quantity = order.quantity
                    product.quantity += quantity
                    db.session.delete(order)
                    db.session.commit()
                    return jsonify({'message': 'Order removed successfully'})

        elif 'update' in data:
            order_id = int(data['update'])
            quantity = float(data['quantity'])
            order = Order.query.filter_by(id=order_id, user_id=user_id).first()
            if order:
                old_quantity = order.quantity
                order.quantity = quantity
                order.total = order.product_price * order.quantity
                product = Product.query.filter_by(id=order.product_id).first()
                product.quantity = product.quantity + old_quantity - order.quantity

                db.session.commit()

                return jsonify({'message': 'Order updated successfully'})

        elif 'buyall' in data:
            orders = Order.query.filter_by(user_id=user_id, status='NC').all()
            for order in orders:
                product = Product.query.filter_by(id=order.product_id).first()
                product.sold_quantity += order.quantity
            for order in orders:
                product_id = order.product_id
                quantity = order.quantity
                product = Product.query.filter_by(id=product_id).first()
                original_quantity = order.quantity

                if original_quantity != quantity:
                    product.quantity = product.quantity + original_quantity - quantity
                    order.quantity = quantity
                    order.total = quantity * order.product_price

                order.status = 'Purchased'

            db.session.commit()

            return jsonify({'message': 'All orders purchased successfully'})


@app.route('/api/customer/<int:user_id>/search', methods=['POST'])
def search_products(user_id):
    search_query = request.json.get('search_query')
    try:
        price = float(search_query)
        products = Product.query.filter_by(price=price).all()
    except ValueError:
        products = Product.query.outerjoin(Categories).filter(
            (Categories.name.ilike(f'%{search_query}%')) |
            (Product.name.ilike(f'%{search_query}%')) |
            (Product.manufacture_date == search_query)
        ).all()
    product_list = [
        {
            'id': product.id,
            'name': product.name,
            'category': product.category.name,
            'price': product.price,
            'unit': product.unit,
            'manufacture_date': product.manufacture_date.strftime('%Y-%m-%d'),
            'quantity': product.quantity
        }
        for product in products
    ]

    return jsonify(product_list)

# Store Manager signup endpoint


@app.route('/store_manager/signup', methods=['POST'])
def store_manager_signup():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    secret_key = data.get('secret_key')
    email = data.get('email')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(secret_key=secret_key.lower()).first():
        return jsonify({'message': 'Secret key already exists'}), 400
    user = User(name=name, username=username, email=email, password=generate_password_hash(
        password), role='store_manager', approved=False, secret_key=secret_key.lower())
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Store Manager signup request submitted. Waiting for admin approval.'}), 201


@app.route('/store_manager/login', methods=['POST'])
def store_manager_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    secret_key = data.get('secret_key')

    user = User.query.filter_by(
        username=username, role='store_manager', secret_key=secret_key).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    if not user:
        return jsonify({'message': 'Please Signup First'}), 402
    if not user.approved:
        return jsonify({'message': 'Wait for confirmation from the admin'}), 403

    access_token = create_access_token(
        identity=user.id, expires_delta=timedelta(days=1))
    user_info = {
        'user_id': user.id,
        'username': user.username,
        'name': user.name,
        'role': user.role,
    }

    return jsonify({'access_token': access_token, 'user': user_info}), 200


def get_user_role():
    identity = get_jwt_identity()
    user = User.query.get(identity)

    if user:
        return user.role
    else:
        return None


@app.route('/api/store-manager/<int:user_id>/product_management', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def product_management(user_id):
    user_role = get_user_role()
    if user_role != 'store_manager':
        return jsonify({"message": "Access denied. User must be a store manager."}), 403

    if request.method == 'GET':
        categories = Categories.query.all()
        categories_data = [{'id': category.id, 'name': category.name}
                           for category in categories]

        products = Product.query.filter_by(created_user_id=user_id).all()
        products_data = [{
            'id': product.id,
            'name': product.name,
            'category_id': product.category_id,
            'expiry_date': product.expiry_date.strftime('%Y-%m-%d'),
            'manufacture_date': product.manufacture_date.strftime('%Y-%m-%d'),
            'price': product.price,
            'unit': product.unit,
            'quantity': product.quantity,
            'created_at': product.created_at.isoformat()
        } for product in products]
        return jsonify({
            'categories': categories_data,
            'products': products_data
        })
    elif request.method == 'DELETE':
        product_id = request.json.get('id')
        product = Product.query.filter_by(
            id=product_id, created_user_id=user_id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"message": "Product removed successfully!"})
        else:
            return jsonify({"error": "Product not found or you are not authorized to delete it."}), 404
    elif request.method == 'PUT':
        updated_product = request.json
        product_id = updated_product.get('id')
        expiry_date = datetime.strptime(
            updated_product.get('expiry_date'), '%Y-%m-%d').date()
        manufacture_date = datetime.strptime(
            updated_product.get('manufacture_date'), '%Y-%m-%d').date()
        product = Product.query.filter_by(
            id=product_id, created_user_id=user_id).first()
        if product:
            product.name = updated_product.get('name', product.name)
            product.category_id = updated_product.get(
                'category_id', product.category_id)
            product.expiry_date = expiry_date
            product.manufacture_date = manufacture_date
            product.price = updated_product.get('price', product.price)
            product.unit = updated_product.get('unit', product.unit)
            product.quantity = updated_product.get(
                'quantity', product.quantity)
            db.session.commit()
            return jsonify({"message": "Product updated successfully!"})
        else:
            return jsonify({"error": "Product not found or you are not authorized to update it."}), 404

    elif request.method == 'POST':
        new_product_data = request.json
        expiry_date = datetime.strptime(
            new_product_data.get('expiry_date'), '%Y-%m-%d').date()
        manufacture_date = datetime.strptime(
            new_product_data.get('manufacture_date'), '%Y-%m-%d').date()

        new_product_name = new_product_data.get('name', '').lower()
        existing_product = Product.query.filter(and_(db.func.lower(
            Product.name) == new_product_name, Product.created_user_id == user_id)).first()
        if existing_product:
            return jsonify({"error": "Product with the same name already exists."}), 409

        new_product = Product(
            name=new_product_data.get('name'),
            category_id=new_product_data.get('category_id'),
            expiry_date=expiry_date,
            manufacture_date=manufacture_date,
            price=new_product_data.get('price'),
            unit=new_product_data.get('unit'),
            quantity=new_product_data.get('quantity'),
            created_user_id=user_id,
            sold_quantity=0,
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product added successfully!"})


@app.route('/export/<int:user_id>/report', methods=['POST'])
@jwt_required()
def export_products(user_id):
    user_role = get_user_role()
    if user_role != 'store_manager':
        return jsonify({"message": "Access denied. User must be a store manager."}), 403
    current_user_id = get_jwt_identity()

    if current_user_id != user_id:
        return jsonify({"message": "Access denied. You can only export your own products."}), 403

    try:

        from tasks import export_product_details_as_csv

        csv_data = export_product_details_as_csv(user_id)
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment; filename=product_report.csv"
        response.headers["Content-type"] = "text/csv"
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/store_manager/<int:user_id>/request', methods=['POST'])
def submit_request(user_id):
    try:
        request_data = request.get_json()

        new_request = Request(
            user_id=18,
            options=request_data.get('option'),
            category=request_data.get('category'),
            modification=request_data.get('newApp'),
            generated_user_id=user_id,
        )

        db.session.add(new_request)
        db.session.commit()

        response_data = {'message': 'Request submitted successfully'}
        return jsonify(response_data), 200
    except Exception as e:
        print('Error submitting request:', e)
        return jsonify({'error': 'An error occurred while submitting the request'}), 500


def check_admin_role():
    current_user = get_jwt_identity()
    if current_user:
        user = User.query.filter_by(id=current_user).first()
        if user and user.role == 'admin':
            return True
    return False


@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    secret_key = data.get('secret_key')

    user = User.query.filter_by(
        username=username, role='admin', secret_key=secret_key).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(
        identity=user.id, expires_delta=timedelta(days=1))
    user_info = {
        'user_id': user.id,
        'username': user.username,
        'name': user.name,
        'role': user.role,
    }

    return jsonify({'access_token': access_token, 'user': user_info}), 200


@app.route('/api/admin/pending_managers', methods=['GET', 'POST'])
@jwt_required()
def get_pending_managers():
    if not check_admin_role():
        return jsonify({"message": "Access denied. User must be an admin."}), 403

    if request.method == 'POST':
        data = request.get_json()
        manager_id = data.get('manager_id')
        status = data.get('status')

        if not manager_id or status not in ['approve', 'reject']:
            return jsonify({'message': 'Invalid request data'}), 400

        user = User.query.get(manager_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        if status == 'approve':
            user.approved = True
        elif status == 'reject':
            db.session.delete(user)

        db.session.commit()

        return jsonify({'message': 'Manager action successfully processed'}), 200
    pending_managers = User.query.filter_by(
        approved=False, role='store_manager').all()

    pending_managers_data = []

    for manager in pending_managers:
        manager_data = {
            'id': manager.id,
            'name': manager.name,
            'email': manager.email,
            'username': manager.username,
        }
        pending_managers_data.append(manager_data)

    return jsonify(pending_managers_data)


@app.route('/api/admin/categories', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def category_management():
    if not check_admin_role():
        return jsonify({"message": "Access denied. User must be an admin."}), 403

    if request.method == 'GET':
        categories = Categories.query.all()
        categories_data = [{'id': category.id, 'name': category.name}
                           for category in categories]

        return jsonify({
            'categories': categories_data
        })
    elif request.method == 'POST':
        data = request.get_json()
        category_name = data.get('name')

        if not category_name:
            return jsonify({"message": "Category name is required."}), 400

        new_category = Categories(name=category_name)
        db.session.add(new_category)
        db.session.commit()

        return jsonify({"message": "Category created successfully.", "category": {"id": new_category.id, "name": new_category.name}}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        category_id = data.get('id')
        category_name = data.get('name')

        if not category_id or not category_name:
            return jsonify({"message": "Category ID and name are required."}), 400

        category = Categories.query.get(category_id)
        if not category:
            return jsonify({"message": "Category not found."}), 404

        category.name = category_name
        db.session.commit()

        return jsonify({"message": "Category updated successfully.", "category": {"id": category.id, "name": category.name}})

    elif request.method == 'DELETE':
        data = request.get_json()
        category_id = data.get('id')

        if not category_id:
            return jsonify({"message": "Category ID is required."}), 400
        category = Categories.query.get(category_id)
        if not category:
            return jsonify({"message": "Category not found."}), 404
        products_to_delete = Product.query.filter_by(
            category_id=category_id).all()
        for product in products_to_delete:
            db.session.delete(product)
        db.session.delete(category)
        db.session.commit()

        return jsonify({"message": "Category deleted successfully."}), 200


@app.route('/api/admin/tasks', methods=['GET', 'DELETE'])
def get_tasks():
    if request.method == 'GET':
        try:
            # Retrieve all tasks from the Request table
            tasks = Request.query.all()

            # Convert the data to a list of dictionaries
            tasks_data = [
                {
                    'id': task.id,
                    'options': task.options,
                    'category': task.category,
                    'modification': task.modification,
                    'generated_user_id': task.generated_user_id
                }
                for task in tasks
            ]

            return jsonify({'tasks': tasks_data})

        except Exception as e:
            return jsonify({'error': str(e)})

    elif request.method == 'DELETE':
        data = request.get_json()
        task_id = data.get('name')
        request1 = Request.query.get(task_id)
        if not request1:
            return jsonify({"message": "Task not found"}), 404
        db.session.delete(request1)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully."}), 200


@app.route('/api/check_login', methods=['GET'])
@cache.cached(timeout=2)
@jwt_required(optional=True)
def check_login():
    current_user = get_jwt_identity()
    if current_user:
        user = User.query.filter_by(username=current_user).first()
        return jsonify({'logged_in': True, 'user': {'username': user.username, 'name': user.name}})
    else:
        return jsonify({'logged_in': False})


if __name__ == '__main__':
    app.run(port=8000)

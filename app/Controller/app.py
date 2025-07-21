import sys, os
# allow imports from sibling folders
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import asyncio

# Import domain logic
from app.Model.problem_model import PowerOperation, FibonacciOperation, FactorialOperation
from app.Model.schema import PowerInput, FibonacciInput, FactorialInput
#from workers import enqueue_task, start_worker
from app.Controller.workers import enqueue_task, start_worker


dirpath = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(dirpath, '..'))

# --- Flask App Setup ---
app = Flask(
    __name__,
    template_folder=os.path.join(project_root, 'View', 'Html'),
    static_folder=os.path.join(project_root, 'View'),
    static_url_path='/static'

)

CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret')

# --- Oracle Database Connection ---
# Install with: pip install oracledb flask_sqlalchemy
oracle_user    = os.environ.get("ORACLE_USER", "py_app")
oracle_pass    = os.environ.get("ORACLE_PASSWORD", "py_app_password")
oracle_host    = os.environ.get("ORACLE_HOST", "oracle-db-api")
oracle_port    = int(os.environ.get("ORACLE_PORT", "1521"))
oracle_service = os.environ.get("ORACLE_SERVICE", "xepdb1")

# build a TNS descriptor with service_name

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"oracle+oracledb://{oracle_user}:{oracle_pass}"
    f"@oracle-db-api:1521/?service_name=xepdb1"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

try:
    with app.app_context():
        result = db.session.execute(text("SELECT 'Connection successful!' FROM DUAL")).scalar()
        print(f"✅ DB Test: {result}")
except Exception as e:
    print(f"❌ DB connection failed: {e}")
# ---------------------------

# Create and start the async worker
loop = asyncio.get_event_loop()
loop.create_task(start_worker())

# --- Math Operation Endpoints ---
@app.route('/pow', methods=['POST'])
def pow_route():
    # Log the API call
    username = request.cookies.get('username', 'anonymous')
    db.session.execute(
    text(
        "INSERT INTO logs (username, endpoint, timestamp) "
        "VALUES (:username, :endpoint, SYSTIMESTAMP)"
    ),
    {"username": username, "endpoint": "pow"}
)
    db.session.commit()

    try:
        data = PowerInput.parse_obj(request.get_json())
        op = PowerOperation(data.base, data.exponent)
        result = loop.run_until_complete(enqueue_task(op.compute))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/fibonacci', methods=['POST'])
def fibonacci_route():
    # Log the API call
    username = request.cookies.get('username', 'anonymous')
    db.session.execute(
    text(
        "INSERT INTO logs (username, endpoint, timestamp) "
        "VALUES (:username, :endpoint, SYSTIMESTAMP)"
    ),
    {"username": username, "endpoint": "fibonacci"}
)
    db.session.commit()

    try:
        data = FibonacciInput.parse_obj(request.get_json())
        op = FibonacciOperation(data.n)
        result = loop.run_until_complete(enqueue_task(op.compute))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/factorial', methods=['POST'])
def factorial_route():
    # Log the API call
    username = request.cookies.get('username', 'anonymous')
    db.session.execute(
    text(
        "INSERT INTO logs (username, endpoint, timestamp) "
        "VALUES (:username, :endpoint, SYSTIMESTAMP)"
    ),
    {"username": username, "endpoint": "factorial"}
)
    db.session.commit()

    try:
        data = FactorialInput.parse_obj(request.get_json())
        op = FactorialOperation(data.n)
        result = loop.run_until_complete(enqueue_task(op.compute))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    try:
        # simple Oracle “ping”
        result = db.session.execute(text("SELECT 1 FROM DUAL")).scalar()
        return jsonify({'status': 'up', 'db': result}), 200
    except Exception as e:
        return jsonify({'status': 'db-error', 'error': str(e)}), 500


# --- Auth Blueprint ---
from app.Controller.auth_controller import auth_bp
from app.Model.user_model import db as user_db

# Initialize User DB models

app.register_blueprint(auth_bp, url_prefix='/auth')
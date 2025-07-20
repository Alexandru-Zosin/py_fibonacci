import sys, os
# allow imports from sibling folders
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import oracledb
import asyncio

# Import domain logic
from Model.problem_model import PowerOperation, FibonacciOperation, FactorialOperation
from Model.schema import PowerInput, FibonacciInput, FactorialInput
#from workers import enqueue_task, start_worker
from Controller.workers import enqueue_task, start_worker


# --- Flask App Setup ---
app = Flask(__name__, template_folder='../View')
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret')

# --- Oracle Database Connection ---
# Install with: pip install oracledb flask_sqlalchemy
oracle_user = os.environ.get('ORACLE_USER', 'your_user')
oracle_pass = os.environ.get('ORACLE_PASSWORD', 'your_password')
oracle_host = os.environ.get('ORACLE_HOST', 'localhost')
oracle_port = os.environ.get('ORACLE_PORT', '1521')
oracle_service = os.environ.get('ORACLE_SERVICE', 'ORCLPDB1')

# Build DSN and SQLAlchemy URI
dsn = oracledb.makedsn(oracle_host, int(oracle_port), service_name=oracle_service)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"oracle+oracledb://{oracle_user}:{oracle_pass}@{dsn}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)
# ---------------------------

# Create and start the async worker
loop = asyncio.get_event_loop()
loop.create_task(start_worker())

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
from auth_controller import auth_bp
from Model.user_model import db as user_db

# Initialize User DB models

app.register_blueprint(auth_bp, url_prefix='/auth')
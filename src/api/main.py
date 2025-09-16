from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from functools import wraps
import logging
import os
import base64
from datetime import datetime, timedelta
from functools import wraps
from src.services.patient_insights import get_patient_insights, format_insights

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Authentication configuration
API_USERNAME = os.getenv('API_USERNAME', 'admin')
API_PASSWORD = os.getenv('API_PASSWORD', 'admin123')
TOKEN_EXPIRATION_HOURS = 24

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    }
)

# JWT Secret Key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=TOKEN_EXPIRATION_HOURS)

# Constants
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10
MAX_PER_PAGE = 100

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Token is missing',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
            
        try:
            # In a real app, you would validate the JWT token here
            # For simplicity, we're using a basic check
            if token != base64.b64encode(f"{API_USERNAME}:{API_PASSWORD}".encode()).decode():
                raise ValueError('Invalid token')
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Invalid token',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
            
        return f(*args, **kwargs)
    return decorated

# Error handling decorator
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    return wrapper

def paginate_results(results, page, per_page):
    """Paginate the query results"""
    total = len(results)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    return {
        'items': results[start_idx:end_idx],
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page
    }

@app.route('/api/auth/login', methods=['POST'])
@handle_errors
def login():
    """
    Authenticate user and return access token
    ---
    tags:
      - Authentication
    parameters:
      - name: credentials
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: admin123
    responses:
      200:
        description: Authentication successful
        schema:
          type: object
          properties:
            access_token:
              type: string
            expires_in:
              type: integer
      401:
        description: Invalid credentials
    """
    auth = request.get_json()
    
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({
            'success': False,
            'error': 'Could not verify',
            'message': 'Username and password are required'
        }), 401
        
    if auth['username'] != API_USERNAME or auth['password'] != API_PASSWORD:
        return jsonify({
            'success': False,
            'error': 'Invalid credentials',
            'message': 'Invalid username or password'
        }), 401
        
    # In a real app, you would generate a JWT token here
    # For simplicity, we're using a base64 encoded string of username:password
    token = base64.b64encode(f"{API_USERNAME}:{API_PASSWORD}".encode()).decode()
    
    return jsonify({
        'success': True,
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': TOKEN_EXPIRATION_HOURS * 3600,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/health')
@handle_errors
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - System
    responses:
      200:
        description: System status
        schema:
          type: object
          properties:
            status:
              type: string
            timestamp:
              type: string
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/patient_insights')
@token_required
@handle_errors
def patient_insights():
    """
    Get paginated patient insights
    Query Parameters:
        page: Page number (default: 1)
        per_page: Items per page (default: 10, max: 100)
    """
    try:
        # Get pagination parameters
        page = int(request.args.get('page', DEFAULT_PAGE))
        per_page = min(int(request.args.get('per_page', DEFAULT_PER_PAGE)), MAX_PER_PAGE)
        
        if page < 1 or per_page < 1:
            raise ValueError("Page and per_page must be positive integers")
            
        # Fetch and format insights
        logger.info(f"Fetching patient insights (page: {page}, per_page: {per_page})")
        results = get_patient_insights()
        formatted_insights = format_insights(results)
        
        # Paginate results
        paginated = paginate_results(formatted_insights, page, per_page)
        
        return jsonify({
            'success': True,
            'data': paginated['items'],
            'pagination': {
                'page': paginated['page'],
                'per_page': paginated['per_page'],
                'total_items': paginated['total'],
                'total_pages': paginated['pages']
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValueError as ve:
        logger.warning(f"Invalid request parameters: {str(ve)}")
        return jsonify({
            'success': False,
            'error': str(ve),
            'timestamp': datetime.utcnow().isoformat()
        }), 400

if __name__ == "__main__":
    logger.info("Starting Doctors Copilot API server...")
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for, flash, session
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# ---------------------------
# ROUTES
# ---------------------------

# database configuration---------------------------------------
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
db_username = os.getenv('DB_USERNAME', 'root')
db_password = os.getenv('DB_PASSWORD', '')
db_host = os.getenv('DB_HOST', 'localhost')
db_name = os.getenv('DB_NAME', 'smartupcycle')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Defining model class for the 'signup' table
class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Defining model class for the 'login' table
class login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


#Singup 
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_signup = Signup(username=username, email=email, password=password)
        db.session.add(new_signup)
        db.session.commit()

        return send_from_directory('frontend', 'login.html')  # Redirect to login page after signup

    return send_from_directory('frontend', 'signup.html')  # Show signup form if GET request


@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Signup.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = user.username
            flash('Login successful!', 'success')
            return send_from_directory('frontend','index.html')
        else:
            flash('Invalid username or password', 'danger')
            return send_from_directory('frontend','login.html')

    return send_from_directory('frontend','login.html')


# Home page
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# DIY Suggestion Route
@app.route('/diy', methods=['POST'])
def diy_suggestions():
    data = request.json
    description = data.get('description', '').strip().lower()

    suggestions = {
        "plastic bottle": {
            "text": "Cut it in half and make a self-watering planter or a pencil holder!",
            "image": "static\media\image4.jpg",
            "tutorial": "https://youtube.com/shorts/_IdoumClpz4?si=o7rX7a4Jqez2p4ao"
        },
        "ice cream sticks": {
            "text": "Create miniature furniture, bookmarks, or even wall art with some glue and paint.",
            "image": "static\media\ice_cream_sticks.jpg",
            "tutorial": "https://youtube.com/shorts/sddGPkdvFTc?si=GQ7hpVeaX0Hv4-rR"
        },
        "old t-shirt": {
            "text": "Turn it into a no-sew tote bag by cutting and knotting the bottom!",
            "image": "static\media\image5.jpg",
            "tutorial": "https://youtube.com/shorts/B72ReAwQ2KI?si=9nKh3jNHrUrw3pQ4"
        },
        "old pant": {
            "text": "Cut the legs into pockets for a tool belt or stitch a denim pouch.",
            "image": "static\media\Denim_pouch.jpeg",
            "tutorial": "https://youtube.com/shorts/paKEMLhKol8?si=EVA89VkEGw8BMFrv"
        },
        "cup": {
            "text": "Paint it to make a decorative candle holder or seed starter!",
            "image": "static\media\candle_holder.jpg",
            "tutorial": "https://youtube.com/shorts/z49UeB2Sk6s?si=jjRv9fuENT0L0V70"
        },
        "cups": {
            "text": "Paint them to make decorative candle holders or seed starters!",
            "image": "static\media\seed_starter.jpeg",
            "tutorial" : "https://youtube.com/shorts/hsJtEOhKy54?si=gdKj9-6zymXu1VPu"
        }
    }

    result = suggestions.get(description)

    if result:
        return jsonify({
            'suggestion': result["text"],
            'image': result["image"],
            'tutorial': result["tutorial"]  
        })
    else:
        return jsonify({
            'suggestion': "Try again 🫤",
            'image': None
        })



# Carbon Analyzer Route

@app.route('/carbon', methods=['POST'])
def analyze_carbon():
    # data = request.json
    # electricity = float(data.get('electricity', 0))  # kWh/month
    # meals = int(data.get('meals', 0))                # meals/week
    # travel = float(data.get('travel', 0))            # km/week
    data = request.json
    print("Received Data:", data)  # 🔍 Log the incoming payload

    try:
        electricity = float(data.get('electricity', 0))
        meals = int(data.get('meals', 0))
        travel = float(data.get('travel', 0))
    except Exception as e:
        return jsonify({"error": str(e), "data": data}), 400

    
    co2_electricity = electricity * 0.85
    co2_meals = meals * 2.5
    co2_travel = travel * 0.21
    co2_total = co2_electricity + co2_meals + co2_travel

   
    electricity_suggestions = [
        "Switch to LED bulbs",
        "Unplug devices when not in use",
        "Use natural light during the day",
        "Use energy-efficient appliances",
        "Install a solar panel for water heating"
    ]

    meal_suggestions = [
        "Try 2 vegetarian days a week",
        "Reduce red meat consumption",
        "Replace meat with legumes once a day",
        "Opt for plant-based dairy alternatives",
        "Support local, organic farms"
    ]

    travel_suggestions = [
        "Use public transport twice a week",
        "Cycle or walk short distances",
        "Carpool with colleagues or friends",
        "Plan your errands in one trip",
        "Switch to electric vehicles when possible"
    ]

    annual_emission = co2_total * 12
    trees_needed = round(annual_emission / 21)

    return jsonify({
        'footprint_kg': round(co2_total, 2),
        'trees_to_offset': trees_needed,
        'suggestions': {
            'electricity': random.sample(electricity_suggestions, 2),
            'meals': random.sample(meal_suggestions, 2),
            'travel': random.sample(travel_suggestions, 2)
        }
    })

# Marketplace upload handler
@app.route('/marketplace', methods=['POST'])
def post_diy_item():
    title = request.form.get('title')
    description = request.form.get('description')
    file = request.files.get('file')

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    return jsonify({'message': 'DIY item uploaded successfully!'})


@app.route('/<path:filename>')
def serve_frontend(filename):
    return send_from_directory(app.static_folder, filename)

# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)

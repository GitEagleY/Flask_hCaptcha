from flask import Flask, render_template, request,  jsonify
import requests

app = Flask(__name__)

# Replace with your actual hCaptcha keys
SITE_KEY = 'your_key'
SECRET_KEY = 'your_key'
VERIFY_URL = 'https://hcaptcha.com/siteverify'

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html', site_key=SITE_KEY)


@app.route("/sign-user-up", methods=['POST'])
def sign_up_user():
    secret_response = request.form['h-captcha-response']

    # Verify the hCaptcha response
    verify_response = requests.post(VERIFY_URL, data={
        'secret': SECRET_KEY,
        'response': secret_response
    }).json()

    if not verify_response.get('success', False):
        # If the verification fails, return a 401 response for AJAX
        return jsonify({'success': False, 'message': 'Captcha validation failed. Please try again.'}), 401

    # Return a success response for AJAX
    return jsonify({'success': True, 'message': 'Registration successful!'})


if __name__ == '__main__':
    app.run(debug=True)

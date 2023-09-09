# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, request, session, redirect, url_for
import random  # Import the random module for generating OTPs
import smtplib  # Import the smtplib module for sending emails
from email.mime.text import MIMEText  # Import MIMEText for email content

# Create a Flask application instance
app = Flask(__name__)

# Set a secret key for the Flask app to enable session usage (Replace 'your_secret_key' with your actual secret key)
app.secret_key = '123456'



# Replace these values with your email server settings
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server hostname (e.g., 'smtp.example.com')
EMAIL_PORT = 587  # Port for SMTP server (587 is the default for TLS)
EMAIL_USERNAME = 'cclass043@gmail.com'  # Your email address for sending OTPs
EMAIL_PASSWORD = 'zxcvbnm@123'  # Your email password or application-specific password

# Define a function to send OTP emails
def send_otp_email(email, otp):
    # Create an email message with the OTP
    msg = MIMEText(f'Your OTP is: {otp}')
    msg['Subject'] = 'OTP Verification'  # Set the email subject
    msg['From'] = 'cclass043@gmail.com'  # Your email address
    msg['To'] = email  # Recipient's email address

    try:
        # Connect to the SMTP server, start TLS encryption, and log in
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        # Send the email and quit the SMTP server connection
        server.sendmail('cclass043@gmail.com', [email], msg.as_string())
        server.quit()
        return True  # Email sent successfully
    except Exception as e:
        print(str(e))  # Print any error messages to the console
        return False  # Email sending failed

# Define a route for the home page
@app.route('/')
def index():
    return render_template('index.html')  # Render the 'index.html' template

# Define a route for handling the form submission to request an OTP
@app.route('/verify', methods=['POST'])
def verify():
    email = request.form['email']  # Get the email address entered in the form
    otp = random.randint(1000, 9999)  # Generate a random OTP
    session['otp'] = otp  # Store the OTP in the session
    session['email'] = email  # Store the email in the session

    # Attempt to send the OTP email
    if send_otp_email(email, otp):
        return redirect(url_for('validate'))  # Redirect to the OTP validation page
    else:
        return "Failed to send OTP. Check your email settings."  # Display an error message

# Define a route for handling the OTP validation form submission
@app.route('/validate', methods=['POST'])
def validate():
    user_otp = int(request.form['OTP'])  # Get the OTP entered by the user
    if 'otp' in session and 'email' in session:
        if user_otp == session['otp']:
            return "OTP verification successful!"  # Display a success message
        else:
            return "Invalid OTP. Try again."  # Display an error message for invalid OTP
    else:
        return redirect(url_for('index'))  # Redirect to the home page if session data is missing

# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
  # Run the app in debug mode for development

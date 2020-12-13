import config
from flask import render_template


# Create the application instance
connex_app = config.connex_app

# Read swagger.yml file to configure the end points.
connex_app.add_api("swagger.yml")

# Create a URL route in our application for "/"
@connex_app.route('/')
def home():
    return render_template('home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    connex_app.run(debug=True)

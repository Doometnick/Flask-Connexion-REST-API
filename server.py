import connexion
from flask import Flask, render_template


# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# Read swagger.yml file to configure the end points.
app.add_api("swagger.yml")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    return render_template('home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

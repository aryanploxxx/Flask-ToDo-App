# This is the code for a flask minimal app
from flask import Flask

app = Flask(__name__)

# Default page
@app.route('/')
def hello_world():
    return 'Hello, World!'

# If anyone visits http://127.0.0.1:5000/products they will be displayed the following message
@app.route('/products')
def products():
    return 'this is products page'
    # Just a text will be printed

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, port=8000)
        # If we want to use any other port apart from the default port-5000
# Previous two lines are essential to run the code otherwise coe will compile but not run
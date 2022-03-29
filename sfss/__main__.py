from sfss import *

FLASK_PORT = 8081

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT, host='0.0.0.0', use_reloader=False)
    #app.run(debug=True, port=FLASK_PORT, use_reloader=False)
    #app.run(debug=True, port=FLASK_PORT)
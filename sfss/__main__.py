from sfss import app, db
from courses_database_conversion import Courses

FLASK_PORT = 8081

app.run(debug=True, port=FLASK_PORT, host='0.0.0.0')
from flask import Flask

from Routes.Home.Home import home_bp
from Routes.GST.Gst import gst_bp
from Routes.GST.Certificate.Compliance.Compliance import table_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(gst_bp)
app.register_blueprint(table_bp)

if __name__ == '__main__':
    app.run(port=8081)

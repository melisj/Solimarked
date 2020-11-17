from app import app
from app.classes.parser import Parser

if __name__ == '__main__':
    parser = Parser()
    parser.set_log_levels()
    app.run(debug=True)

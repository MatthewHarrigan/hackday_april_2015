from flask import Flask
app = Flask(__name__)

@app.route('/page/<page>')
def show_user_profile(page):
    return 'User %s' % page

if __name__ == '__main__':
    app.run()
    app.debug = True

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DevNotebook</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8 text-center">
                    <h1 class="display-4 mb-4">Welcome to DevNotebook</h1>
                    <p class="lead">Your productivity companion is ready to be built.</p>
                    <p class="text-muted">The migration to Replit is complete. You can now start building your application.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

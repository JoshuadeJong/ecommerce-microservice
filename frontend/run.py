from app.main import create_app

app = create_app()
app.run(host="0.0.0.0", port=5600, debug=True)

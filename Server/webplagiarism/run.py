from plagiarism_webapp import create_app  # sto facendo l'import dall' init file di quel package plagiarism_webapp

app = create_app()  # nessun parametro, usiamo config

if __name__ == '__main__':
    #app.run(debug=True)
    from waitress import serve
    serve(app,host="localhost",port=5000)

from __init__ import create_app

app = create_app()

if __name__ == "__main__":
    # HTTPS 사용 시
    app.run(
        host='0.0.0.0', 
        port=5001, 
        debug=True,
        ssl_context=('cert.pem', 'key.pem')  # SSL 인증서 사용
    )
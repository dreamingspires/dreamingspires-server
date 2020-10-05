from app import app, socketio

def main():
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()

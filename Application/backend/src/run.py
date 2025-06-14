from src.controllers.Controller import app
from src.services.MQTTListener import main
import threading

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=main)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    app.run(debug=True, host='0.0.0.0', port=5000)
from api_wmiys import app 
from api_wmiys.common import constants, user_image

if __name__ == "__main__":
    user_image.STATIC_URL_PREFIX = constants.DevConfig.STATIC_URL_PREFIX.value
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
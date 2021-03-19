import uvicorn
from api.app import app
from api.config import ConfigFast

uvicorn.run(app, host='0.0.0.0', port=ConfigFast.PORT)

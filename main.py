import os
import uvicorn
from app.api import app


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80 if os.getenv("APP_ENVIRONMENT") == "production" else 8000, log_level='info')
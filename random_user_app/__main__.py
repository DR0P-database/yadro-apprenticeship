import uvicorn

from random_user_app.routes.base import app

if __name__ == "__main__":
    uvicorn.run(app)

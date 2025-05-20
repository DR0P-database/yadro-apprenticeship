import uvicorn

if __name__ == "__main__":
    uvicorn.run("random_user_app.routes.base:app", reload=True)
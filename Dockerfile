FROM python:3.9-slim

WORKDIR /yadro_apprenticeship

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY random_user_app ./random_user_app 

EXPOSE 8000

CMD ["uvicorn", "random_user_app.routes.base:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
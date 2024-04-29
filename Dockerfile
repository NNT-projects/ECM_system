FROM python:3.11.7

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .
COPY utils.py data_preprocessing.py .  # Include utils.py if used by inference_pipeline.py
COPY . .

# Replace 'your_model.pkl' with the actual model file path within the container
# This assumes your model is saved as a pickle file
CMD ["python", "src/inference_pipeline.py", "--model_path=/app/your_model.pkl"]

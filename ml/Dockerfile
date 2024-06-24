# ML DOCKERFILE

# docker build -t my_project_image .
# docker run -v /Users/riter/Development/python-workspace/s7_pipelines/data:/app/data my_project_image


# Use an official Python runtime as a parent image
FROM python:3.11.7

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run inference_pipeline.py when the container launches
CMD ["python", "src/inference_pipeline.py"]


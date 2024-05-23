
#
FROM python:3.9

#
WORKDIR /code

#
COPY ./back/ECM_system/requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./back/ECM_system /code/app

EXPOSE 8000

#
CMD ["uvicorn", "app.main:app",  "--port", "8000"]

######

# docker build -t my_project_image .
# docker run -v /Users/riter/Development/python-workspace/s7_pipelines/data:/app/data my_project_image


# Use an official Python runtime as a parent image
# FROM python:3.11.7

# Set the working directory in the container
# WORKDIR /app

# Copy the current directory contents into the container at /app
# COPY . /app

# Install any needed dependencies specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Run inference_pipeline.py when the container launches
# CMD ["python", "src/inference_pipeline.py"]


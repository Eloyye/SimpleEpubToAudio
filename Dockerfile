# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make sure the environment is activated:
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["conda", "run", "-n", "base", "python", "src/app.py"]
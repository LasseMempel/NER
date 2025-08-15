FROM continuumio/anaconda3:latest

WORKDIR /app

# Copy environment file and create conda environment
COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "ner-backend", "/bin/bash", "-c"]

# Make conda available in PATH
ENV PATH /opt/conda/envs/ner-backend/bin:$PATH

# Copy app
COPY app/ app/
COPY main.py app/main.py

# Expose port
EXPOSE 8000

# Run server
CMD ["conda", "run", "-n", "ner-backend", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
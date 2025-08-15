FROM continuumio/anaconda3:latest

WORKDIR /app

# Copy environment and create conda env
COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "ner-backend", "/bin/bash", "-c"]

# Install git-lfs if needed (for large files in future)
RUN apt-get update && apt-get install -y git-lfs && rm -rf /var/lib/apt/lists/*

# Activate environment
ENV PATH /opt/conda/envs/ner-backend/bin:$PATH

# Copy preload script
COPY preload_model.py .

# Pre-download GLiNER model
RUN conda run -n ner-backend python preload_model.py

# Copy app code
COPY app/ app/

# Expose port
EXPOSE 8000

# Run with async worker (uvicorn)
CMD ["conda", "run", "-n", "ner-backend", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
FROM python:3.11-slim

# Hugging Face Spaces runs as a non-root user (UID 1000)
# We need to set this up so app.py has permissions to write to drives.json
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY --chown=user . .

EXPOSE 7860

CMD ["python", "app.py"]

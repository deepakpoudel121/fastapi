# Step 1 — choose a base image
# "slim" = minimal Debian Linux with Python, no bloat
FROM python:3.13-slim

# Step 2 — set the working directory inside the container
# All future commands run from here
WORKDIR /app

# Step 3 — copy ONLY requirements first (layer caching trick)
COPY requirements.txt .

# Step 4 — install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5 — now copy the rest of your code
COPY . .

# Step 6 — tell Docker what port the app listens on (documentation only)
EXPOSE 8000

# Step 7 — the command to start your app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
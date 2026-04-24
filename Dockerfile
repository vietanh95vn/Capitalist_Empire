# 1. Base Image: We use the official Playwright image because installing Chromium OS-level dependencies on a raw Linux box is a nightmare.
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# 2. Set the working directory inside the Container
WORKDIR /app

# 3. Cache Optimization: Copy requirements FIRST to leverage Docker Layer Caching
COPY requirements.txt .

# 4. Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire Capitalist Empire into the Container
COPY . .

# 6. Expose the API Port
EXPOSE 8000

# 7. The Ignition Command: Boot up the Uvicorn Server, bind it to 0.0.0.0 so it can communicate with the outside world
CMD ["uvicorn", "serving_layer.api:app", "--host", "0.0.0.0", "--port", "8000"]
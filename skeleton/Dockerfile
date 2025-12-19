# 1. Base Image: Use a lightweight Python version
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of our code into the container
COPY . .

# 6. Define the command to run our app
# We use 'python' to execute the script
CMD ["python", "skeleton_nf.py"]
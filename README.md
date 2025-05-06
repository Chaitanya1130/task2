# Deployment Steps

This document outlines the steps to deploy a FastAPI application using Docker, Google Cloud Run, and GitHub Actions for CI/CD. Follow these steps to ensure a smooth deployment process.

---

## Step 1: Create `requirements.txt` File
The first step is to capture all the necessary dependencies for the project. The `requirements.txt` file ensures that the exact same libraries and their versions used during development can be installed in the deployment environment, guaranteeing consistency.

Run the following command in the project's root directory to generate the file:
```bash
pip freeze > requirements.txt
```

---

## Step 2: Create the Dockerfile
A `Dockerfile` is required to build a container image for the FastAPI application. This image will bundle the application code, runtime environment, libraries, and dependencies into a portable unit.

Here’s a sample `Dockerfile` for a typical FastAPI application:

```dockerfile
# Specifies the base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the application dependencies listed in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that your FastAPI application runs on (default: 8000)
EXPOSE 8000

# Define the command to start your FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Step 3: Create the `.dockerignore` File
To optimize the Docker image build process and reduce the size of the final image, create a `.dockerignore` file. This file specifies files and directories that Docker should exclude when copying project files into the container image.

Here’s a typical `.dockerignore` file for a Python-based FastAPI project:

```
.git          # Excludes git repository
__pycache__   # Excludes Python metadata
*.pyc
*.log         # Prevents any log files from local development
venv          # Excludes your local virtual environment
.env          # Ignores environment variable files that might contain sensitive information
```

---

## Step 4: Build the Docker Image
Build the Docker image using the following command:
```bash
docker build -t your_app_name:latest .
```

---

## Step 5: Run the Docker Container
Run the Docker container with the following command:
```bash
docker run -d -p 8000:8000 --name your_container_name your_app_name:latest
```

To include environment variables, use the `--env-file` option:
```bash
docker run -d -p 8000:8000 --env-file .env --name your_container_name your_app_name:latest
```

---

## Step 6: Test Locally Using Postman
Test the application locally using the URL `http://localhost:8000/`. Ensure that the routes match the exact paths for testing:

- `http://localhost:8000/text/changetoUpperCase`
- `http://localhost:8000/text/changetoLowerCase`
- `http://localhost:8000/text/reverseText`
- `http://localhost:8000/text/countWordsandCharacters`

---

## Step 7: Deploy the Container to Google Cloud Run
1. Tag the Docker image:
   ```bash
   docker tag your_app_name:latest asia-south1-docker.pkg.dev/id/repo-name/your_app_name:latest
   ```

2. Push the tagged image to the Google Artifact Registry:
   ```bash
   docker push asia-south1-docker.pkg.dev/id/repo-name/your_app_name
   ```

3. Deploy the container to Google Cloud Run:
   ```bash
   gcloud run deploy service-name \
       --image asia-south1-docker.pkg.dev/id/repo-name/your_app_name:latest \
       --region asia-south1 \
       --platform managed \
       --allow-unauthenticated
   ```

4. After deployment, you will receive a public URL. Use this URL for testing:
   - Example: `https://fastapi-service-backend-181462483271.asia-south1.run.app`
   - Test the routes using the same paths as in Step 6.

---

## Step 8: Adding Cloud Logs and Viewing Them
### Adding Logs
To enable logging in your FastAPI application, use Python’s `logging` module. Add the following code to your application:

```python
import logging

# Create a logger instance
logger = logging.getLogger(__name__)

# Use logging methods
logger.info("This is an info log")
logger.warning("This is a warning log")
logger.error("This is an error log")
logger.debug("This is a debug log")
```

### Viewing Logs
1. Go to the Google Cloud Console.
2. Navigate to **Cloud Run**.
3. Select the deployed service.
4. Open the **Logs** tab to view the application logs.

---

## Step 9: Automating Build, Push, and Deployment with GitHub Actions
To automate the deployment process, set up a GitHub Actions workflow. This ensures continuous integration (CI) and continuous deployment (CD) whenever code is pushed to the main branch.

### Prerequisites
1. A Google Cloud Project (e.g., `tasktwochaitanya`).
2. A GKE cluster and Cloud Run service.
3. A GitHub repository with the FastAPI code.
4. A Service Account with permissions for GKE, Cloud Run, and Artifact Registry.
5. GitHub Secrets configured for `GCP_SA_KEY`.

### GitHub Actions Workflow
Here’s a sample workflow file (`.github/workflows/deploy.yml`):

```yaml
name: Deploy FastAPI App

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Google Cloud credentials
      uses: google-github-actions/auth@v1
      with:
        credentials_json: ${{ secrets.GCP_SA_KEY }}

    - name: Set up Docker
      uses: docker/setup-buildx-action@v3

    - name: Authenticate Docker with Artifact Registry
      run: gcloud auth configure-docker asia-south1-docker.pkg.dev

    - name: Build Docker image
      run: docker build -t asia-south1-docker.pkg.dev/tasktwochaitanya/fastapi-repo/fastapi-image:latest .

    - name: Push Docker image
      run: docker push asia-south1-docker.pkg.dev/tasktwochaitanya/fastapi-repo/fastapi-image:latest

    - name: Deploy to Cloud Run
      run: gcloud run deploy fastapi-service \
        --image asia-south1-docker.pkg.dev/tasktwochaitanya/fastapi-repo/fastapi-image:latest \
        --region asia-south1 \
        --platform managed \
        --allow-unauthenticated
```

---

## Step 10: YAML Files for Kubernetes
To deploy the application on GKE, use the following YAML files:

### `deployment.yaml`
Defines the Kubernetes Deployment for the application:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
      - name: fastapi-container
        image: asia-south1-docker.pkg.dev/tasktwochaitanya/fastapi-repo/fastapi-image:latest
        ports:
        - containerPort: 8000
```

### `service.yaml`
Defines the Kubernetes Service to expose the application:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

---

## Step 11: Verify Deployment
1. **GitHub Actions**: Check the **Actions** tab in your GitHub repository to confirm that the workflow ran successfully.
2. **Cloud Run**: Visit the public URL provided by Cloud Run to verify the application is running.



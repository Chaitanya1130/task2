# Deployment Steps

## Step 1: Create `requirements.txt` file
- After receiving the FastAPI template, the first step is to capture all the necessary dependencies for the project. The `requirements.txt` file ensures that the exact same libraries and their versions used during development can be installed in the deployment environment, guaranteeing consistency.
- This can be achieved using the following command in the project's root directory:
  ```bash
  pip freeze > requirements.txt
  ```

---

## Step 2: Create the Dockerfile
- The next step is to create a `Dockerfile`. This file contains a set of instructions for Docker to build a container image for your FastAPI application. The container image bundles your application code, runtime environment, libraries, and dependencies into a portable unit.
- Here's a sample `Dockerfile` for a typical FastAPI application:

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

  # Expose the port that your FastAPI application runs on (usually 8000)
  EXPOSE 8000

  # Define the command to start your FastAPI application
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```

---

## Step 3: Create the `.dockerignore` file
- To optimize the Docker image build process and reduce the size of your final image, create a `.dockerignore` file. This file specifies files and directories that Docker should exclude when copying your project files into the container image.

- Here's a typical `.dockerignore` file for a Python-based FastAPI project:

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
- Build the Docker image with the following command:
  ```bash
  docker build -t your_app_name:latest .
  ```

---

## Step 5: Run the Docker Container
- Run the Docker container with the following command:
  ```bash
  docker run -d -p 8000:8000 --name your_container_name your_app_name:latest
  ```
- You can also define environment variables using the `--env-file .env` option.

---

## Step 6: Testing Locally in `Postman`
- Test your application locally using the URL `http://localhost:8000/`.
- Ensure the routes match the exact paths for testing locally:
  - `http://localhost:8000/text/changetoUpperCase`
  - `http://localhost:8000/text/changetoLowerCase`
  - `http://localhost:8000/text/reverseText`
  - `http://localhost:8000/text/countWordsandCharacters`

---

## Step 7: Deploying the Container to `Google Cloud Run`
1. After the image has been successfully built, tag the image with the following command:
   ```bash
   docker tag your_app_name:latest asia-south1-docker.pkg.dev/id/repo-name/your_app_name:latest
   ```
2. Push the tagged image to the container registry:
   ```bash
   docker push asia-south1-docker.pkg.dev/id/repo-name/your_app_name
   ```
3. Deploy the container to Cloud Run using the following command:
   ```bash
   gcloud run deploy service-name \
       --image asia-south1-docker.pkg.dev/id/repo-name/your_app_name:latest \
       --region asia-south1 \
       --platform managed \
       --allow-unauthenticated
   ```
4. After successful deployment, you will receive a public URL. Use this URL for testing:
   - Example: `https://fastapi-service-backend-181462483271.asia-south1.run.app`
   - Test the routes using the same paths:
     - `url/text/changetoUpperCase`
     - `url/text/changetoLowerCase`
     - `url/text/reverseText`
     - `url/text/countWordsandCharacters`

---

## Step 8: Adding Cloud Logs and Viewing Them
### Adding Logs
- Import the `logging` module.
- Create a logger instance using:
  ```python
  logger = logging.getLogger(__name__)
  ```
- Use logging methods such as:
  - `logger.info()`
  - `logger.warning()`
  - `logger.error()`
  - `logger.debug()`

### Viewing Logs
- Go to Cloud Run.
- Select the service.
- Open the "Logs" tab.
- View the logs.

---

## Step 9: Automating Build, Push, and Deployment
### Necessary Pre-Steps
1. A Google Cloud Project (e.g., `tasktwochaitanya`).
2. GKE cluster created.
3. Cloud Run service ready.
4. A GitHub repository (e.g., `Chaitanya1130/task2`) with the FastAPI code.
5. A Service Account with permissions for GKE, Cloud Run, and Artifact Registry.

### Steps
1. Build and push the Docker image:
   ```bash
   docker build -t asia-south1-docker.pkg.dev/tasktwochaitanya/fastapi-repo/y-fastapi-image:latest .
   docker push asia-south1-docker.pkg.dev/tasktwochaitanya/fastapi-repo/y-fastapi-image:latest
   ```
2. Configure for GKE using `kustomization.yaml`:
   ```yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization

   resources:
     - deployment.yaml
     - service.yaml

   images:
     - name: fastapi-app-gke
       newName: asia-south1-docker.pkg.dev/tasktwochaitanya/fastapi-repo/y-fastapi-image
       newTag: latest

   patches:
     - target:
         kind: Deployment
         name: fastapi-app-gke
       patch: |-
         - op: replace
           path: /spec/template/spec/containers/0/image
           value: asia-south1-docker.pkg.dev/tasktwochaitanya/fastapi-repo/y-fastapi-image:${{ IMAGE_TAG }}
   ```
3. Set up GitHub Actions Workflow:
   ```yaml
   on:
     push:
       branches:
         - main

   jobs:
     deploy:
       runs-on: ubuntu-latest
       env:
         GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GCP_SA_KEY }}
         PROJECT_ID: tasktwochaitanya
         REGION: asia-south1
         SERVICE_NAME: fastapi-service-backend
         IMAGE: y-fastapi-image
         GAR_LOCATION: asia-south1
         REPOSITORY: fastapi-repo
   ```

---

## Step 10: YAML Files
- Configured Kubernetes using `deployment.yaml` and `service.yaml` to define the app setup and service exposure. A `kustomization.yaml` was used to patch the container image dynamically during the CI/CD pipeline. This setup allows the GitHub Actions workflow to update only the image tag and apply the new configuration without rewriting the manifests.

### Key Files:
1. **`deployment.yaml`**:
   - Defines:
     - Container image
     - Exposed port
     - Environment variables
     - Kubernetes Deployment for `fastapi-app-gke`

2. **`service.yaml`**:
   - Connects to pods with the label `app: fastapi-app-gke`.

3. **`kustomization.yaml`**:
   - Specifies:
     - Resources to apply (`deployment.yaml`, `service.yaml`).
     - Dynamic patching of the container image.
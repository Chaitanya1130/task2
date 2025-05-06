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

  # Installs the application dependencies listed in requirements.txt
  RUN pip install --upgrade pip && pip install -r requirements.txt

  # Copy the application code into the container
  COPY . .

  # Expose the port that your FastAPI application runs on (usually 8000)
  EXPOSE portNumber

  # Defines the command to start your FastAPI application. It uses Uvicorn, an ASGI server, and specifies the host, port, and the location of your FastAPI app (main:app).
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
  docker run -d -p host_port:container_port --name your_container_name your_app_name:latest
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
   docker tag image-name:latest asia-south1-docker.pkg.dev/id/repo-name/image-name:latest
   ```
2. Push the tagged image to the container registry:
   ```bash
   docker push asia-south1-docker.pkg.dev/id/repo-name/image-name
   ```
3. Deploy the container to Cloud Run using the following command:
   ```bash
   gcloud run deploy service-name \
       --image asia-south1-docker.pkg.dev/id/repo-name/image-name:latest \
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

## Step 9: Automating build,push and deployment
###hello
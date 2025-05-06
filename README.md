# Deployment Steps

- **Step 1: Create `requirements.txt` file**
  - After receiving the FastAPI template, the first step is to capture all the necessary dependencies for the project. The `requirements.txt` file ensures that the exact same libraries and their versions used during development can be installed in the deployment environment, guaranteeing consistency.
  - This can be achieved using the following command in the project's root directory:
    ```bash
    pip freeze > requirements.txt
    ```

- **Step 2: Create the Dockerfile**
  - The next step is to create a `Dockerfile`. This file contains a set of instructions for Docker to build a container image for your FastAPI application. The container image bundles your application code, runtime environment, libraries, and dependencies into a portable unit.
  -Here's a sample `Dockerfile` for a typical FastAPI application:

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
 
- **Step 3: Create the `.dockerignore` file**
  - To optimize the Docker image build process and reduce the size of your final image. This file specifies files and directories that Docker should exclude when copying your project files into the container image. 

  - Here's a typical `.dockerignore` file for a Python-based FastAPI project:

    ```
    .git --> excludes git repository
    __pycache__ --> excludes python metadata
    *.pyc
    *.log --> prevents any log files from local development
    venv --> excludes your local virtual environment
    .env --> Ignores environment variable files that might contain sensitive information.
    ```

- **Step 4 : Build the Docker Image**
    -Build it with the command:
    ```bash
        docker build -t your_app_name:latest .
    ```
-**Step 5: Run the Docker Container**
    -Run it with the command:
    '''bash
        docker run -d -p host_port:container_port --name your_container_name your_app_name:latest
    '''
    -You can also define the env variables (--env-file .env)
-**Step 6 : Testing locally in `Postman`**
    -From the local url i.e http://localhost:8000/.. we can test our application and check if it is working properly
    -The routes must match the exact paths for testing locally as mentioned below:
        -http://localhost:8000/text/changetoUpperCase
        -http://localhost:8000/text/changetoLowerCase
        -http://localhost:8000/text/reverseText
        -http://localhost:8000/text/countWordsandCharacters
        
        
-**Step 7 : Deploying the container to `Google cloud Run`**
    - After the image has been successfully built with the command 
    '''bash
        docker build -t image-name .
    '''
    -The next step is to tag the image which can be done with the follwing command 
    '''bash
        docker tag image-name:latest asia-south1-docker.pkg.dev/id/repo-name/image-name:latest
    '''
    -Finally to push the above tag/artifact we have to follow the command
    '''bash
        docker push asia-south1-docker.pkg.dev/id/repo-name/image-name
    '''
    -Now the artifact has been successfully pushed to the container, we have to deploy the container to cloud run using the follwing command 
    '''bash
        gcloud run deploy service-name     --image asia-south1-docker.pkg.dev/id/repo-name/image-name:latest     --region asia-south1     --platform managed     --allow-unauthenticated
    '''
    -The id and repository name can be obtained at the time of creating the new project. 
    -After successful execution we will receive a public url, this public url can be used for testing like this:
        -https://fastapi-service-backend-181462483271.asia-south1.run.app
        -To test this we have to follow the same exact routes:
            -url/text/changetoUpperCase
            -url/text/changetoLowerCase
            -url/text/reverseText
            -url/text/countWordsandCharacters
-**Step 8 : Adding Cloud logs and Viewing them**:
    -Adding 
        -import logging module
        -create a logger instance using the command logging.getLogger(__name__)
        -methods of logging are logger.info(),logger.warning(),logger.error(),logger.debug()
    -Viewing
        -go to cloud run 
        -select service
        -open logs tab
        -view logs

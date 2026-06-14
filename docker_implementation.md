If you want to test the Docker integration locally on your Windows machine, you must install a container engine. Docker Desktop is the standard and most
  straightforward way to do this on Windows.

  Here is the step-by-step process to get Docker running and test your application:

  Step 1: Install Docker Desktop
   1. Download the installer from the official Docker website: Docker Desktop for Windows (https://docs.docker.com/desktop/install/windows-install/).
   2. Run the installer. When prompted, ensure that the option to Use WSL 2 instead of Hyper-V is checked (this is the recommended backend for better
      performance).
   3. Follow the installation wizard to completion.
   4. Restart your computer if the installer prompts you to do so.

  Step 2: Start Docker Desktop
   1. After restarting, open the Docker Desktop application from your Windows Start menu.
   2. Accept the terms and conditions if prompted.
   3. Wait for the Docker engine to start. You will see a green icon or a "Running" status in the bottom-left corner of the Docker Desktop window.

  Step 3: Test Your Application using Docker Compose
  Once Docker is running, you can build and launch your application using the terminal.

   1. Open your terminal (Git Bash or PowerShell) and navigate to your project root folder (D:\Projects\DL_assigment02).
   2. Run the following command to build the container images and start the services:
   1    docker-compose up --build
   3. Docker will begin downloading the base Python images, installing your requirements, and setting up the network. This might take a few minutes the
      first time.
   4. Once it finishes, you should see logs from both the frontend and backend services in your terminal.

  Step 4: Access the Application
   - Frontend (Streamlit): Open your web browser and go to http://localhost:8501. You should see your Tea Leaf Disease Classifier UI.
   - Backend API (FastAPI): You can view the API documentation at http://localhost:8000/docs.

  Step 5: Shutting Down
  To stop the application, go back to the terminal where docker-compose is running and press Ctrl + C. Then, to clean up the containers, run:
   1 docker-compose down

  Note: If you are unable to install Docker Desktop due to system restrictions, you can skip local Docker testing. The Dockerfile and docker-compose.yml we
  created are standard and ready for deployment to cloud platforms (like Render or Railway) that will build the Docker images for you
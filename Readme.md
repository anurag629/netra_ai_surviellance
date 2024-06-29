# Advanced Computer Vision Surveillance System

This project is an advanced computer vision surveillance system that allows for real-time monitoring, face recognition, and location tracking. The system includes features for managing cameras and persons, and displays the last known locations of identified persons on a map.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features

- **Real-time Camera Feed**: Stream video from multiple cameras.
- **Face Recognition**: Identify known persons using face recognition.
- **Location Tracking**: Track the last known locations of identified persons.
- **Person Management**: Add, edit, and delete person details.
- **Camera Management**: Add, edit, and delete camera details.
- **Location Map**: Display the last known locations of identified persons on a map with detailed information.

## Tech Stack

- **Frontend**: React, Tailwind CSS
- **Backend**: FastAPI
- **Database**: SQLite
- **Computer Vision**: OpenCV, YOLO, face_recognition
- **Deployment**: Docker, Azure

## Setup

### Prerequisites

- Node.js
- Python 3.7+
- Docker (optional for containerized deployment)

### Backend Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/surveillance-system.git
    cd surveillance-system
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Download YOLO configuration and weights files**:
    - Download `yolov3.cfg` from: https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg
    - Download `yolov3.weights` from: https://pjreddie.com/media/files/yolov3.weights
    - Download `coco.names` from: https://github.com/pjreddie/darknet/blob/master/data/coco.names

    Place these files in a directory named `backend/app/yolo` inside the project root directory.

5. **Run the FastAPI server**:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend Setup

1. **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```

2. **Install the required npm packages**:
    ```bash
    npm install
    ```

3. **Start the React development server**:
    ```bash
    npm start
    ```

### Docker Setup (Optional)

1. **Build the Docker image**:
    ```bash
    docker build -t surveillance-system .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -p 8000:8000 surveillance-system
    ```

## Usage

1. **Access the application**:
   Open your browser and navigate to `http://localhost:3000` to access the frontend.

2. **Navigate to the Dashboard**:
   The dashboard displays the real-time camera feed and the location map.

3. **Manage Persons and Cameras**:
   Navigate to the "Manage" section from the navbar to add, edit, or delete persons and cameras.

## API Endpoints

### Persons

- **GET /persons**: Get a list of all persons.
- **POST /persons**: Add a new person.
- **DELETE /persons/{person_id}**: Delete a person by ID.

### Cameras

- **GET /cameras**: Get a list of all cameras.
- **POST /cameras**: Add a new camera.
- **DELETE /cameras/{camera_id}**: Delete a camera by ID.

### Locations

- **GET /locations**: Get a list of all locations.
- **GET /locations/person/{person_id}**: Get locations for a specific person.

## License

This project is licensed under the MIT License.

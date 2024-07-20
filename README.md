# EaseAttend

EaseAttend is an open-source computer software designed to capture faces and record attendance using facial recognition technology. The software leverages the `face_recognition` and `cv2` libraries to identify individuals and maintain attendance records.

## Features

- Real-time face detection and recognition using a webcam.
- Attendance recording with the option to mark detected and absent faces.
- Generates CSV files for present and absent attendees.
- Easy to set up and use.

## Prerequisites

- Python 3.x
- `face_recognition` library
- `opencv-python` library
- `numpy` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/EaseAttend.git
    cd EaseAttend
    ```

2. Install the required libraries:

    ```sh
    pip install face_recognition opencv-python numpy
    ```

## Usage

1. Prepare the images of the people you want to recognize and save them in the same directory as the script. Update the script to load these images and their corresponding names.

2. Run the script:

    ```sh
    python easeattend.py
    ```

3. The script will start the webcam and begin detecting faces. Detected faces will be displayed on the screen with their names.

4. To exit the script, press `q` on the keyboard.

5. The script will generate two CSV files: one for presentees and one for absentees, saved with the current date in their filenames.

## Code Overview

Here's a brief overview of the main sections of the code:

- **Imports and Initialization**: The required libraries are imported, and the webcam is initialized.
- **Loading Known Faces**: The script loads images of known faces and encodes them.
- **Face Detection and Recognition**: The script captures frames from the webcam, detects faces, and matches them against the known faces.
- **Display Results**: The recognized faces are displayed with their names.
- **Save Attendance Records**: At the end of the session, the script saves the list of detected faces (presentees) and undetected faces (absentees) to CSV files.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to improve the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The `face_recognition` library by Adam Geitgey: https://github.com/ageitgey/face_recognition
- OpenCV library: https://opencv.org/

## Contact

For any inquiries or feedback, please reach out to [your email].

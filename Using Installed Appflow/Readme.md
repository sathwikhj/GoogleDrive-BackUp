## Google Drive Backup Docker Image for Oauth Client

This Dockerfile creates an image that allows you to run a Python script for backing up files to Google Drive using the Google Drive API.

### Prerequisites to Dokcerize the file

Before building and running the Docker image, make sure you have the following:

- Docker installed on your system.
- `main.py` and `credentials.json` files in the same directory as this Dockerfile.
- Python script (`main.py`) for Google Drive backup.

### Usage

- Run it once to generate the `api_tokens.json` to avoid authentication when in the docker container
  ```bash
  python main.py
  ```

- Build the container
  ```bash
  docker build -t <image_name> .
  ```
- Run the container
  ```bash
  docker build -t <image_name> .
  ```

### Changes to be make before running

You need to replace the following placeholders with your local paths:

- Replace <main.py> with the local path to your main.py file.
- Replace <local_path_to_credenti.json> with the local path to your credenti.json file.
- Replace <local_path_to_api_tokens.json> with the local path to your api_tokens.json file.
  
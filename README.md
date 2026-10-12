# CS408-Final-Project

Python/Django web application deployed on AWS EC2.

## Requirements

- Python 3.12 (Python 3.10+ minimum)
- Python venv support
- Internet connection for installing dependencies

## Running Locally

Clone the repository and run:

    ./start.sh

Then open http://127.0.0.1:8000/

## Deployment

The application runs on Ubuntu EC2 using nginx, Gunicorn, and systemd.

Deploy from a local machine:

    ./deploy/deploy.sh -h PUBLIC-IP -i PATH-TO-KEY.pem

The setup script is located at `deploy/setup-ec2.sh`.

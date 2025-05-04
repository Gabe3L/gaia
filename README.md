# Project GAIA

GAIA (Gabe's AI Assistant) is an AI-powered desktop assistant that enables intuitive hands-free human-computer interaction. It uses voice recognition to interpret spoken requests, tracks hand gestures to control the cursor, and speaks responses aloud using a text-to-speech engine.

GAIA aims to be a fully hands-free assistant useful for accessibility, productivity, and interactive environments, including robotics and human-machine collaboration.

## Features

- **Voice Command Recognition**  
  Natural Language Processing (NLP) powered by speech recognition allows users to control the assistant through voice commands.

- **Cursor Control via Hand Gestures**  
  Leverages computer vision and hand tracking to manipulate the mouse pointer using hand motions captured by a webcam.

- **Text-to-Speech Feedback**  
  GAIA responds verbally to user requests using a realistic voice engine, completing the interaction loop.

## Prerequisites

Ensure the following are installed on your system:

- [Python 3.12+](https://www.python.org/downloads/)
- [CUDA 12.6+](https://developer.nvidia.com/cuda-toolkit-archive/) (Optional)
- Pip package manager (`pip`)
- A webcam (internal or USB)
- A working microphone

## Installation Guide

Clone GAIA from GitHub:

```bash
git clone https://github.com/Gabe3L/gaia.git
cd gaia
```

Activate a virtual environment and install dependancies:
```bash
pip install --upgrade pip
pip install virtualenv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Once installation and hardware setup are complete, run the program:

```bash
python -m main.py
```

# Permissions and Privacy
When first running GAIA, your operating system may prompt for permission to access:

- Microphone
- Camera

On Windows, grant access by visiting:

- ```Settings > Privacy & Security > Microphone```
- ```Settings > Privacy & Security > Camera```

# Troubleshooting

| **Issue**                        | **Solution**                                                                     |
|----------------------------------|----------------------------------------------------------------------------------|
| Microphone not detected          | Ensure it is the default input device and that the volume is appropriate         |
| Webcam not opening               | Check if it's being used by another app or blocked in Camera Settings            |
| Hand tracking is slow or laggy   | Improve lighting and ensure CUDA is installed                                    |
| Text-to-speech is silent         | Ensure your speaker is set as the default audio output                           |
| Running scripts is disabled      | Run ```Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process``` in terminal |
| General Issue                    | Check the log files located in logs/files                                        |

# Current Features
- Google Calendar
- Web Search (Google, Wikipedia, YouTube)
- Geolocation and Local Weather Reports
- News Briefs and Updates
- Website Launcher
- Sending Emails
- Spotify Integration
- Note Taking Utility
- Date & Time Reporting
- System Resource Monitoring
- Voice Typing

# Planned Features

Planned features for upcoming versions of GAIA include:

- IoT integration for smart home control
- HUD available through a shortcut
- Personalized assistant profiles
- Metal GPU Support

# License
This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for more information.

# Support
For questions, support, or collaboration inquiries, please contact:

Project Maintainer: Gabe Lynch

## Contact Info
- GitHub: https://github.com/Gabe3L/
- Website: https://www.gabelynch.com/
- Email: contact@gabelynch.com

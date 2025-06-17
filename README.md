# Project GAIA

GAIA (Gabe's AI Assistant) is an intelligent, voice-activated desktop assistant that enables intuitive hands-free human-computer interaction. It uses voice recognition to interpret spoken requests and delivers clear, natural responses aloud using a text-to-speech engine.

GAIA aims to be a fully hands-free assistant useful for accessibility, productivity, and interactive environments, including robotics and human-machine collaboration.

## Features

- **Voice Command Recognition**  
  Natural Language Processing (NLP) powered by speech recognition allows users to control the assistant through voice commands.

- **Text-to-Speech Feedback**  
  GAIA responds verbally to user requests using a realistic voice engine, completing the interaction loop.

- **Responsive and Customizable UI**
  All features of the app are viewable and customizable through a modern and clean user interface.

## Prerequisites

### Software

- **Operating System**:  
  - **Windows** (10/11)
  - **macOS** (Ventura, Sonoma, Sequoia)
  - **Linux** (Ubuntu 22.04, other distributions may work with adjustments)

- **Python 3.12+**:  
  - Ensure Python 3.12 or later is installed for backend functionality.  
  - [Download Python](https://www.python.org/downloads/)

- **CUDA 12.6+ (Optional but Recommended)**:  
  - CUDA is required for GPU acceleration, improving performance for tasks like hand gesture tracking.  
  - [Download CUDA](https://developer.nvidia.com/cuda-toolkit-archive/)

- **Node.js LTS v22**:  
  - Node.js is required for the frontend (Electron).  
  - [Download Node.js](https://nodejs.org/en/download)

### Peripherals
  
- **Microphone**:
  - **Recommended**: Clear microphone for high accuracy
  - **Optional**: Disable "Voice Input" in settings

- **Audio Output**:  
  - **Recommended**: Built-in speakers or headphones
  - **Optional**: Disable "Voice Output" in settings

- **Display**:
  - **Recommended**: 1080p (FHD) Resolution or Higher
  - **Optional**: Tell GAIA "Disable Display"

### Hardware

- **Processor (CPU)**:
  - **Minimum**: Quad-core, 2.5 GHz
  - **Recommended**: Eight core, 3GHz

- **RAM**:  
  - **Minimum**: 8 GB
  - **Recommended**: 16 GB+

- **Storage**:  
  - **Minimum**: 10 GB of free disk space  
  - **Recommended**: SSD for faster load times

- **Graphics Processing Unit (GPU)**:
  - **Recommended**: A modern GPU with CUDA capability (Compute Capability >= 3.0).  
  - **Optional**: GPU acceleration can be disabled, though expect a significant drop in performance

## Installation Guide

Clone GAIA from GitHub:

```bash
git clone https://github.com/Gabe3L/gaia.git
cd gaia
```

### Backend Setup

Activate a virtual environment and install dependancies:
```bash
pip install --upgrade pip
pip install virtualenv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend Setup

Install electron and all other required packages:
```bash
npm install
```

### Starting the program

Once installation and hardware setup are complete, run the program:

```bash
npm start
```

## Permissions and Privacy
When first running GAIA, your operating system may prompt for permission to access:

- Microphone
- Camera

On Windows, grant access by visiting:

- ```Settings > Privacy & Security > Microphone```
- ```Settings > Privacy & Security > Camera```

## Troubleshooting

| **Issue**                        | **Solution**                                                                     |
|----------------------------------|----------------------------------------------------------------------------------|
| Microphone not detected          | Ensure it is the default input device and that the volume is appropriate         |
| Text-to-speech is silent         | Ensure your speaker is set as the default audio output                           |
| Running scripts is disabled      | Run ```Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process``` in terminal |
| Recieved an error message        | Check the log files located in backend/logs/files and contact Gabe Lynch         |

## Current Features
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

## Planned Features

Planned features for upcoming versions of GAIA include:

- IoT integration for smart home control
- Mini HUD available through a shortcut
- Personalized assistant profiles
- Metal GPU Support

## License
This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for more information.

## Support
For questions, support, or collaboration inquiries, please contact Gabe Lynch.

### Contact Info
- GitHub: https://github.com/Gabe3L/
- Website: https://www.gabelynch.com/
- Email: contact@gabelynch.com

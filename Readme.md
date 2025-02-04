# Bureaucratic Productivity Enhancer

## Overview

The Bureaucratic Productivity Enhancer is an integrated suite of tools designed to streamline bureaucratic processes through advanced AI-driven content generation, seamless translation services, and efficient voice dictation capabilities. This application aims to augment productivity within institutional frameworks by providing user-friendly interfaces and robust functionalities tailored for professional environments.

## Repository Structure

The repository is organized into the following directories:

- **AI_content_generator**: Contains modules for generating structured content using AI algorithms.
- **Deployment**: Includes deployment configurations and the main interface for the application.
- **Translator**: Hosts components responsible for language translation services.
- **Voice_Dictation**: Comprises tools for converting voice input into text.

## Setup and Installation

To deploy and run the application, please follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/codegeek03/Bureaucratic_productivity_enhancer.git
   cd Bureaucratic_productivity_enhancer
   ```

2. **Install Dependencies**:
   Ensure that Python is installed on your system. Install the required Python packages using the provided `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Each module contains an `.env` file where you can configure necessary environment variables. Ensure these files are properly set up before running the modules.

## Module Details

### AI Content Generator

**Location**: `AI_content_generator/`

**Description**: This module leverages AI to generate structured and informative content.

**Key Files**:
- `main.py`: Contains FastAPI endpoints for the AI content generation service.
- `contentgen.py`: Implements the core logic for content generation.

**How to Run**:
Navigate to the `AI_content_generator` directory and execute the following command:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 9000
```
This will start the FastAPI server for the AI content generator.

### Translator

**Location**: `Translator/`

**Description**: Provides language translation services through a FastAPI interface.

**Key Files**:
- `api.py`: Contains FastAPI endpoints for translation services.
- `translator.py`: Implements the translation logic.

**How to Run**:
Navigate to the `Translator` directory and execute:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 9001
```
This will start the FastAPI server for the translation service.

### Voice Dictation

**Location**: `Voice_Dictation/`

**Description**: Facilitates the conversion of voice inputs into text.

**Key Files**:
- `main.py`: Contains FastAPI endpoints for voice dictation services.
- `speech_Recog.py`: Handles speech recognition processes.

**How to Run**:
Navigate to the `Voice_Dictation` directory and execute:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 9002
```
This will start the FastAPI server for the voice dictation service.

### Deployment

**Location**: `Deployment/`

**Description**: Contains deployment configurations and the main interface for the application.

**Key Files**:
- `index.html`: The main HTML file for the application's interface.

**How to Run**:
Open `index.html` in a live server environment to view the application on `localhost`.

## Contributing

We welcome contributions from the community to enhance the functionality and efficiency of this application. Please adhere to the following guidelines:

- **Fork the Repository**: Create a personal fork of the repository.
- **Create a Feature Branch**: Develop your feature or fix in a dedicated branch.
- **Submit a Pull Request**: Once your feature is complete, submit a pull request for review.

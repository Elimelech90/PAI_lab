# VISAGE — Face Intelligence & Personality Profiling System
## Lab 6 Task 2 | Programming for Artificial Intelligence

---

## Overview
A Flask-based face profiling web application that:
- Detects faces using OpenCV Haar Cascade classifiers
- Measures facial features (eyes, nose region, mouth, forehead, jawline)
- Generates an annotated image with labeled regions and measurements
- Maps facial geometry to one of the **16 MBTI Personality Types**
- Supports both image upload and live webcam capture

---

## Tech Stack
- **Backend**: Python + Flask
- **Computer Vision**: OpenCV (Haar Cascades for face, eye, smile detection)
- **Frontend**: Vanilla HTML/CSS/JS — no frameworks needed
- **Personality Engine**: Custom scoring algorithm → MBTI mapping

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Flask server
```bash
python app.py
```

### 3. Open in browser
```
http://localhost:5000
```

---

## Features

### Face Detection
- Frontal face detection (haarcascade_frontalface_default)
- Profile face fallback (haarcascade_profileface)
- Eye detection (haarcascade_eye)
- Smile detection (haarcascade_smile)

### Measurements
| Feature | Method |
|---|---|
| Face Shape | Width/Height ratio analysis |
| Eye Spacing | Inter-ocular distance ratio |
| Forehead Height | Upper 35% of face bounding box |
| Jaw Type | Lower face width estimation |
| Smile | Haar cascade on lower face ROI |

### Personality Mapping (16 MBTI Types)
Features are scored and mapped to personality types:
- Face ratio → Introvert/Extrovert lean
- Eye spacing → Intuition/Sensing dimension
- Forehead size → Thinking/Feeling dimension
- Jaw structure → Judging/Perceiving dimension

> **Note**: This is an artistic interpretation for educational purposes, not a scientifically validated personality assessment.

---

## Project Structure
```
face_profiler/
├── app.py              # Flask backend + CV logic
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend (upload, webcam, results)
└── static/             # Static assets folder
```

---

## Usage Tips
- Use a **clear, well-lit frontal photo** for best detection
- Face should occupy at least **30% of the image**
- Avoid heavy filters or extreme angles
- Webcam capture works in modern browsers (HTTPS or localhost)
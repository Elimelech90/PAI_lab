from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import os
import random
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

CASCADE_PATH = cv2.data.haarcascades

face_cascade = cv2.CascadeClassifier(CASCADE_PATH + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(CASCADE_PATH + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(CASCADE_PATH + 'haarcascade_smile.xml')
profile_cascade = cv2.CascadeClassifier(CASCADE_PATH + 'haarcascade_profileface.xml')

MBTI_TYPES = {
    "INTJ": {
        "name": "The Architect",
        "description": "Strategic, independent, decisive, and highly analytical. INTJs are rare masterminds who see the world as a chessboard.",
        "strengths": ["Strategic thinking", "Self-confidence", "High standards", "Independent"],
        "traits": ["Visionary", "Determined", "Private", "Rational"],
        "color": "#1a1a2e"
    },
    "INTP": {
        "name": "The Thinker",
        "description": "Innovative, imaginative, and driven by logic. INTPs love theories and abstract ideas more than socializing.",
        "strengths": ["Analytical", "Open-minded", "Inventive", "Objective"],
        "traits": ["Curious", "Logical", "Reserved", "Flexible"],
        "color": "#16213e"
    },
    "ENTJ": {
        "name": "The Commander",
        "description": "Bold, imaginative, and strong-willed leaders who find a way — or make one.",
        "strengths": ["Leadership", "Confidence", "Efficiency", "Strategic"],
        "traits": ["Decisive", "Ambitious", "Inspiring", "Dominant"],
        "color": "#0f3460"
    },
    "ENTP": {
        "name": "The Debater",
        "description": "Smart and curious thinkers who cannot resist an intellectual challenge.",
        "strengths": ["Charismatic", "Energetic", "Strategic", "Quick-witted"],
        "traits": ["Bold", "Creative", "Sociable", "Irreverent"],
        "color": "#533483"
    },
    "INFJ": {
        "name": "The Advocate",
        "description": "Quiet, mystical yet inspiring and tireless idealists. The rarest personality type.",
        "strengths": ["Insightful", "Principled", "Passionate", "Altruistic"],
        "traits": ["Private", "Perfectionistic", "Sensitive", "Decisive"],
        "color": "#2d6a4f"
    },
    "INFP": {
        "name": "The Mediator",
        "description": "Poetic, kind and altruistic people, always eager to help a good cause.",
        "strengths": ["Empathetic", "Generous", "Creative", "Passionate"],
        "traits": ["Idealistic", "Curious", "Adaptable", "Warm"],
        "color": "#40916c"
    },
    "ENFJ": {
        "name": "The Protagonist",
        "description": "Charismatic and inspiring leaders who captivate their listeners.",
        "strengths": ["Charismatic", "Empathetic", "Reliable", "Tolerant"],
        "traits": ["Natural leader", "Idealistic", "Organized", "Warm"],
        "color": "#1b4332"
    },
    "ENFP": {
        "name": "The Campaigner",
        "description": "Enthusiastic, creative, and sociable free spirits who make a psychic connection with others.",
        "strengths": ["Curious", "Observant", "Energetic", "Enthusiastic"],
        "traits": ["Creative", "Sociable", "Emotional", "Independent"],
        "color": "#52b788"
    },
    "ISTJ": {
        "name": "The Logistician",
        "description": "Practical and fact-minded people whose reliability cannot be doubted.",
        "strengths": ["Honest", "Responsible", "Dependable", "Practical"],
        "traits": ["Calm", "Organized", "Traditional", "Loyal"],
        "color": "#7f5af0"
    },
    "ISFJ": {
        "name": "The Defender",
        "description": "Dedicated and warm protectors, always ready to defend their loved ones.",
        "strengths": ["Supportive", "Reliable", "Patient", "Observant"],
        "traits": ["Humble", "Empathetic", "Hard-working", "Loyal"],
        "color": "#2cb67d"
    },
    "ESTJ": {
        "name": "The Executive",
        "description": "Excellent administrators who are unsurpassed at managing things and people.",
        "strengths": ["Dedicated", "Strong-willed", "Organized", "Honest"],
        "traits": ["Traditional", "Loyal", "Patient", "Reliable"],
        "color": "#ff6b6b"
    },
    "ESFJ": {
        "name": "The Consul",
        "description": "Extraordinarily caring, social and popular people, eager to help.",
        "strengths": ["Caring", "Loyal", "Sociable", "Practical"],
        "traits": ["Warm", "Dutiful", "Popular", "Sensitive"],
        "color": "#ffd166"
    },
    "ISTP": {
        "name": "The Virtuoso",
        "description": "Bold and practical experimenters, masters of all kinds of tools.",
        "strengths": ["Optimistic", "Creative", "Practical", "Relaxed"],
        "traits": ["Observant", "Flexible", "Independent", "Calm"],
        "color": "#118ab2"
    },
    "ISFP": {
        "name": "The Adventurer",
        "description": "Flexible and charming artists, always ready to explore and experience something new.",
        "strengths": ["Charming", "Sensitive", "Artistic", "Imaginative"],
        "traits": ["Curious", "Spontaneous", "Warm", "Creative"],
        "color": "#06d6a0"
    },
    "ESTP": {
        "name": "The Entrepreneur",
        "description": "Smart, energetic people who truly enjoy living on the edge.",
        "strengths": ["Bold", "Rational", "Original", "Perceptive"],
        "traits": ["Direct", "Sociable", "Observant", "Risk-taker"],
        "color": "#ef476f"
    },
    "ESFP": {
        "name": "The Entertainer",
        "description": "Spontaneous, energetic and enthusiastic entertainers. Life is never boring around them.",
        "strengths": ["Bold", "Original", "Aesthetic", "Showmanship"],
        "traits": ["Playful", "Practical", "Observant", "Excellent"],
        "color": "#ffd60a"
    }
}

def analyze_face_features(face_roi, face_rect, gray_img):
    """Analyze facial features and return measurements."""
    x, y, w, h = face_rect
    features = {}

    # Face shape ratio
    face_ratio = w / h
    if face_ratio > 0.90:
        features['face_shape'] = 'Round'
    elif face_ratio > 0.75:
        features['face_shape'] = 'Oval'
    elif face_ratio > 0.65:
        features['face_shape'] = 'Oblong'
    else:
        features['face_shape'] = 'Narrow'

    features['face_width'] = w
    features['face_height'] = h
    features['face_ratio'] = round(face_ratio, 2)

    # Eye detection
    eyes = eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))
    features['eye_count'] = len(eyes)

    if len(eyes) >= 2:
        eyes = sorted(eyes, key=lambda e: e[0])
        eye1, eye2 = eyes[0], eyes[1]
        eye_distance = abs((eye2[0] + eye2[2]//2) - (eye1[0] + eye1[2]//2))
        features['eye_distance'] = eye_distance
        features['eye_distance_ratio'] = round(eye_distance / w, 2)

        # Eye size
        avg_eye_w = (eye1[2] + eye2[2]) / 2
        features['avg_eye_width'] = round(avg_eye_w)
        features['eye_to_face_ratio'] = round(avg_eye_w / w, 2)

        if features['eye_distance_ratio'] > 0.45:
            features['eye_spacing'] = 'Wide-set'
        elif features['eye_distance_ratio'] < 0.30:
            features['eye_spacing'] = 'Close-set'
        else:
            features['eye_spacing'] = 'Normal'
    else:
        features['eye_distance'] = 0
        features['eye_spacing'] = 'Not detected'
        features['eye_distance_ratio'] = 0
        features['avg_eye_width'] = 0
        features['eye_to_face_ratio'] = 0

    # Smile detection
    smile_roi = face_roi[int(h*0.5):, :]
    smiles = smile_cascade.detectMultiScale(smile_roi, scaleFactor=1.7, minNeighbors=20)
    features['smile_detected'] = len(smiles) > 0

    # Nose estimated position (center of face)
    nose_y = int(h * 0.55)
    nose_x = w // 2
    features['nose_position'] = f"Center ({nose_x}, {nose_y})"

    # Forehead ratio
    forehead_height = int(h * 0.35)
    features['forehead_height'] = forehead_height
    features['forehead_ratio'] = round(forehead_height / h, 2)

    if features['forehead_ratio'] > 0.40:
        features['forehead_type'] = 'High forehead'
    elif features['forehead_ratio'] < 0.30:
        features['forehead_type'] = 'Low forehead'
    else:
        features['forehead_type'] = 'Average forehead'

    # Jaw estimation
    jaw_width = int(w * 0.85)
    features['jaw_width'] = jaw_width
    jaw_ratio = jaw_width / w
    if jaw_ratio > 0.90:
        features['jaw_type'] = 'Square jaw'
    elif jaw_ratio > 0.80:
        features['jaw_type'] = 'Defined jaw'
    else:
        features['jaw_type'] = 'Soft jaw'

    return features

def determine_personality(features):
    """Determine MBTI personality type based on facial features."""
    # Use feature-based scoring to select personality type
    # This is a fun/artistic interpretation, not scientifically validated
    score = 0

    # Face shape influence
    if features.get('face_shape') == 'Round':
        score += 2  # More feeling/perception
    elif features.get('face_shape') == 'Oblong':
        score += 6  # More thinking/judging

    # Eye spacing
    if features.get('eye_spacing') == 'Wide-set':
        score += 1
    elif features.get('eye_spacing') == 'Close-set':
        score += 4

    # Forehead
    if features.get('forehead_type') == 'High forehead':
        score += 3
    elif features.get('forehead_type') == 'Low forehead':
        score += 0

    # Smile
    if features.get('smile_detected'):
        score += 1  # Extrovert lean

    # Jaw
    if features.get('jaw_type') == 'Square jaw':
        score += 5
    elif features.get('jaw_type') == 'Soft jaw':
        score += 1

    # Face ratio
    face_ratio = features.get('face_ratio', 0.75)
    if face_ratio > 0.85:
        score += 2

    mbti_list = list(MBTI_TYPES.keys())
    # Map score to MBTI index (0-15)
    idx = min(int(score / 20 * 16), 15)
    # Add slight randomness for variety
    idx = (idx + random.randint(0, 2)) % 16
    return mbti_list[idx]

def draw_face_annotations(img, face_rect, features):
    """Draw bounding boxes and feature annotations on the image."""
    x, y, w, h = face_rect
    annotated = img.copy()

    # Main face rectangle
    cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 150), 2)

    # Face center cross
    cx, cy = x + w//2, y + h//2
    cv2.line(annotated, (cx-15, cy), (cx+15, cy), (0, 200, 255), 1)
    cv2.line(annotated, (cx, cy-15), (cx, cy+15), (0, 200, 255), 1)

    # Forehead line
    forehead_y = y + features.get('forehead_height', 0)
    cv2.line(annotated, (x, forehead_y), (x+w, forehead_y), (255, 200, 0), 1)

    # Eye region highlight
    eye_region_y = y + int(h * 0.25)
    eye_region_h = int(h * 0.35)
    cv2.rectangle(annotated, (x+5, eye_region_y), (x+w-5, eye_region_y+eye_region_h), (100, 100, 255), 1)

    # Nose region
    nose_y = y + int(h * 0.45)
    nose_h = int(h * 0.25)
    nose_x_off = int(w * 0.3)
    cv2.rectangle(annotated, (x+nose_x_off, nose_y), (x+w-nose_x_off, nose_y+nose_h), (255, 100, 100), 1)

    # Mouth/smile region
    mouth_y = y + int(h * 0.65)
    mouth_h = int(h * 0.25)
    mouth_x_off = int(w * 0.15)
    cv2.rectangle(annotated, (x+mouth_x_off, mouth_y), (x+w-mouth_x_off, mouth_y+mouth_h), (100, 255, 200), 1)

    # Labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(annotated, 'Face', (x, y-8), font, 0.5, (0, 255, 150), 1)
    cv2.putText(annotated, 'Eyes', (x+5, eye_region_y-4), font, 0.4, (100, 100, 255), 1)
    cv2.putText(annotated, 'Nose', (x+nose_x_off, nose_y-4), font, 0.4, (255, 100, 100), 1)
    cv2.putText(annotated, 'Mouth', (x+mouth_x_off, mouth_y-4), font, 0.4, (100, 255, 200), 1)
    cv2.putText(annotated, 'Forehead', (x+3, forehead_y-4), font, 0.4, (255, 200, 0), 1)

    # Measurement lines
    # Width measurement
    cv2.line(annotated, (x, y+h+12), (x+w, y+h+12), (200, 200, 200), 1)
    cv2.putText(annotated, f'{w}px', (x + w//2 - 15, y+h+25), font, 0.4, (200, 200, 200), 1)

    return annotated

def process_image(image_data):
    """Process uploaded image and return face analysis results."""
    # Decode base64 image
    if ',' in image_data:
        image_data = image_data.split(',')[1]

    img_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return {'error': 'Could not decode image'}

    # Resize if too large
    max_dim = 800
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w*scale), int(h*scale)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
    )

    if len(faces) == 0:
        # Try profile face detection
        faces = profile_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
        )

    if len(faces) == 0:
        return {'error': 'No face detected. Please upload a clear frontal face photo.'}

    # Analyze the largest face
    largest_face = max(faces, key=lambda f: f[2] * f[3])
    x, y, w_f, h_f = largest_face
    face_roi = gray[y:y+h_f, x:x+w_f]

    # Get features
    features = analyze_face_features(face_roi, largest_face, gray)

    # Determine personality
    personality_key = determine_personality(features)
    personality = MBTI_TYPES[personality_key]

    # Draw annotations
    annotated_img = draw_face_annotations(img, largest_face, features)

    # Convert annotated image to base64
    _, buffer = cv2.imencode('.jpg', annotated_img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    annotated_b64 = base64.b64encode(buffer).decode('utf-8')

    return {
        'success': True,
        'annotated_image': f'data:image/jpeg;base64,{annotated_b64}',
        'face_count': len(faces),
        'features': {
            'Face Shape': features['face_shape'],
            'Face Width': f"{features['face_width']}px",
            'Face Height': f"{features['face_height']}px",
            'Width/Height Ratio': str(features['face_ratio']),
            'Eye Spacing': features['eye_spacing'],
            'Eye Distance Ratio': str(features['eye_distance_ratio']),
            'Avg Eye Width': f"{features['avg_eye_width']}px",
            'Eye-to-Face Ratio': str(features['eye_to_face_ratio']),
            'Forehead Type': features['forehead_type'],
            'Forehead Ratio': str(features['forehead_ratio']),
            'Jaw Type': features['jaw_type'],
            'Smile Detected': 'Yes ✓' if features['smile_detected'] else 'No',
            'Nose Position': features['nose_position'],
        },
        'personality': {
            'mbti': personality_key,
            'name': personality['name'],
            'description': personality['description'],
            'strengths': personality['strengths'],
            'traits': personality['traits'],
            'color': personality['color']
        }
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    result = process_image(data['image'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
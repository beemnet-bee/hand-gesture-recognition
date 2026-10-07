# AetherGesture: AI Hand Gesture Recognition System

A real-time, browser-based and desktop-compatible Computer Vision system that recognizes basic hand gestures using webcam input.

## Features
- **4 Core Gestures**: Open Hand, Fist, Thumbs Up, and Victory/Peace.
- **Extended Gestures**: Pointing, OK Sign, Rock Horns, and Thumbs Down.
- **Real-Time Telemetry**: 60 FPS processing, sub-15ms inference latency, 21-joint 3D coordinate inspection.
- **Biomechanical Analysis**: Live flexion percentage and joint angle calculation.
- **Dual Pipeline Support**:
  1. Web/TypeScript client powered by MediaPipe WebAssembly & HTML5 Canvas.
  2. Standalone Python/OpenCV desktop script using `mediapipe` and `numpy`.

## Quickstart (Web)
```bash
npm install
npm run dev
```

## Quickstart (Python Desktop)
```bash
pip install -r requirements.txt
python main.py
```

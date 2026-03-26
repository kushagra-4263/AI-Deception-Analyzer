# AI Deception Detection using Eye Tracking & Behavior Analysis (ProtoType)

## ❓ Problem Statement
Traditional lie detection methods are intrusive and unreliable. This project explores non-invasive behavioral analysis using computer vision to estimate deception probability.

## 📌 Overview

This project is a real-time computer vision system that analyzes behavioral patterns such as eye blinks and gaze direction to estimate deception probability.

## 🚀 Features

* Real-time face and eye tracking using MediaPipe
* Blink detection using Eye Aspect Ratio (EAR)
* Gaze direction tracking (Left / Right / Center)
* Baseline behavior calibration phase
* Interactive question-response system
* Behavioral scoring based on deviation from baseline
* Result logging to CSV

## ⚙️ System Flow
1. Capture video input
2. Detect face landmarks (MediaPipe)
3. Calculate EAR (blink detection)
4. Track gaze direction
5. Compare with baseline behavior
6. Generate deception score

## ⚠️ Disclaimer

This is a prototype system and not a scientifically validated lie detector.
It demonstrates behavioral analysis using computer vision techniques.

## 🛠️ Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy

## ▶️ How to Run

1. Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/AI-Deception-Analyzer.git
cd AI-Deception-Analyzer
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the project:

```
python main.py
```

## 📊 Output

* Displays real-time deception score
* Shows per-question analysis
* Saves results in `results.csv`

## 🔮 Future Scope

* Machine Learning-based prediction
* Facial expression analysis
* Voice-based stress detection
* Improved accuracy with dataset training

## 👨‍💻 Author

Kushagra Mishra (MCA - AI/ML)

# 🤖 AI Cognitive Agent

An intelligent cognitive assistant that:
- Classifies incoming content (emails, articles, tasks, notes)
- Suggests the best action using a rule-based + RL-enhanced model
- Accepts user feedback to improve over time (Reinforcement Learning)
- Uses **Steganography with AES encryption** to hide classification info in images
- Provides an **interactive dashboard** for simulation & feedback

---

## ✅ Key Features

✔ **Interactive Feedback Loop (👍 / 👎)**  
- Confirm or change the suggested action.
- Reinforcement Learning updates weights dynamically.

✔ **Steganography Component (Enhanced)**  
- Hides action + confidence securely in an image using AES encryption.
- Allows custom image upload or uses a generated image.

✔ **User-Friendly Dashboard**  
- Built with **Streamlit**.
- Includes:
  - Text input area & sample texts
  - Prediction results with reason & confidence
  - RL status and updates
  - Feedback buttons
  - Steganography visualization (embed + extract)

✔ **Action Reasons & RL Updates Visible**  
- Shows why an action was chosen.
- Displays RL weight adjustments after feedback.

✔ **Confidence Feedback Shapes Learning**  
- Positive feedback boosts confidence for correct actions.
- Negative feedback penalizes wrong predictions and boosts chosen action.
- Weights stored in `weights.json` for persistence.

---

## ✅ How It Works

1. **Input Content** → Email, task, article, or note.
2. **Predict Action** → Schedule, Ignore, Mark Important, Summarize.
3. **Feedback** → Confirm (👍) or Change (👎).
4. **RL Learning** → Confidence adjusts over time based on feedback.
5. **Steganography** → Hides classification details in an image.

## Access Dashboard
http://localhost:8501


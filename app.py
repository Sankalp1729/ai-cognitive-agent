import streamlit as st
from cognitive_modules.decision_classifier import DecisionClassifier
from cognitive_modules.feedback_handler import FeedbackHandler
from cognitive_modules.stego_handler import StegoHandler
from settings import USE_FEEDBACK
from PIL import Image
import os
import json

# Initialize modules
classifier = DecisionClassifier()
feedback_handler = FeedbackHandler(classifier)
stego = StegoHandler()

# Streamlit Page Config
st.set_page_config(page_title="AI Cognitive Agent Dashboard", layout="wide")
st.title("🤖 AI-Cognitive-Agent Dashboard")
st.write("Classify text, apply feedback, and embed hidden data using steganography.")

# Sidebar Settings
st.sidebar.header("⚙ Settings")
st.sidebar.write(f"Feedback Learning: {'Enabled ✅' if USE_FEEDBACK else 'Disabled 🚫'}")

# Sample Inputs for Quick Testing
sample_texts = {
    "Meeting Reminder": "Meeting Tomorrow Reminder for the meeting scheduled tomorrow at 10 AM.",
    "Discount Offer": "Special Discount Offer Get 50% off on your next purchase.",
    "Project Task": "Finish project report before Friday.",
    "External Link": "Important link: https://docs.python.org/3/",
    "AI Article": "AI in 2025 Artificial Intelligence is transforming businesses worldwide..."
}

# Input Section
st.header("📥 Input Content")
selected_sample = st.selectbox("Choose a sample text or enter your own:", list(sample_texts.keys()))
content = st.text_area("Enter text (Email, Article, Task, Note):", value=sample_texts[selected_sample], height=150)

# Optional Image Upload
uploaded_img = None
if st.checkbox("Upload a custom image for steganography"):
    uploaded_img = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

# Prediction Section
if st.button("🔍 Predict Action"):
    if content.strip() == "":
        st.error("Please enter some text!")
    else:
        result = classifier.classify({"type": "custom", "content": content})

        # Show prediction details
        st.subheader("✅ Prediction Results")
        st.write(f"**Action:** {result['action']} | **Confidence:** {result['confidence']*100:.2f}%")
        st.write(f"**Reason:** {result['reason']}")

        # RL Status
        rl_status = "Enabled ✅" if USE_FEEDBACK else "Disabled 🚫"
        st.write(f"**Reinforcement Learning:** {rl_status}")

        # Feedback Section
        st.subheader("👍 Provide Feedback")
        col1, col2 = st.columns(2)
        feedback_status = ""
        chosen_action = result['action']

        with col1:
            if st.button("👍 Confirm"):
                feedback_status = "Confirmed 👍"
        with col2:
            if st.button("👎 Change"):
                new_action = st.selectbox("Select New Action", ["Schedule", "Ignore", "Mark Important", "Summarize"])
                chosen_action = new_action
                feedback_status = "Updated 👎"

        # If feedback is given
        if feedback_status:
            st.success(f"Feedback: {feedback_status}, Final Action: {chosen_action}")

            if USE_FEEDBACK:
                feedback_handler.apply_feedback(result['action'], chosen_action)
                st.info(f"RL Update: Adjusted weights. Current weight for {chosen_action}: {classifier.action_weights[chosen_action]:.2f}")
            else:
                st.warning("RL Update: Skipped (Feedback ignored)")

            # Steganography Section
            st.subheader("🔐 Steganography")
            hidden_msg = f"Action: {chosen_action}, Confidence: {result['confidence']:.2f}"
            save_path = "outputs/hidden_output.png"
            os.makedirs("outputs", exist_ok=True)
            base_img = Image.open(uploaded_img) if uploaded_img else None
            stego.embed_message(base_img, save_path, hidden_msg)
            st.image(save_path, caption="Image with Hidden Message", use_column_width=True)

            # Extract hidden message
            extracted = stego.extract_message(save_path)
            st.write(f"🔍 **Extracted Message:** {extracted}")

            # Save logs
            os.makedirs("logs", exist_ok=True)
            log_entry = {
                "input": content,
                "predicted_action": result['action'],
                "final_action": chosen_action,
                "confidence": result['confidence'],
                "reason": result['reason'],
                "feedback_status": feedback_status,
                "reinforcement_learning": "Applied" if USE_FEEDBACK else "Skipped",
                "hidden_image": save_path,
                "hidden_data_verified": extracted
            }
            with open("logs/dashboard_logs.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")

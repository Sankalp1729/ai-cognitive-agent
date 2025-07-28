# main.py
import json
import os
from cognitive_modules.decision_classifier import DecisionClassifier
from cognitive_modules.feedback_handler import FeedbackHandler
from cognitive_modules.stego_handler import StegoHandler

items = [
    {"type": "articles", "content": "AI in 2025 Artificial Intelligence is transforming businesses worldwide..."},
    {"type": "emails", "content": "Meeting Tomorrow Reminder for the meeting scheduled tomorrow at 10 AM."},
    {"type": "emails", "content": "Discount Offer Get 50% off on your next purchase."},
    {"type": "tasks", "content": "Finish Project Report"},
    {"type": "notes", "content": "Important Link https://docs.python.org/3/"}
]

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    classifier = DecisionClassifier()
    feedback_handler = FeedbackHandler()
    stego = StegoHandler()
    logs = []

    for idx, item in enumerate(items, start=1):
        classification = classifier.classify(item)

        print(f"\nItem {idx}: {item['content']}")
        print(f"Predicted Action: {classification['action']}")
        print(f"Confidence: {classification['confidence']}")

        feedback_result = feedback_handler.get_feedback(classification["action"])
        chosen_action = feedback_result["new_action"]

        classification["action"] = chosen_action
        classification["feedback_status"] = feedback_result["status"]

        print(f"✅ Feedback Status: {feedback_result['status']} {feedback_result['emoji']}")

        hidden_msg = f"Action: {classification['action']}, Confidence: {classification['confidence']}"
        img_path = f"outputs/hidden_{item['type']}_{idx}.png"
        stego.embed_message(None, img_path, hidden_msg)
        extracted_msg = stego.extract_message(img_path)

        print(f"✅ Hidden feedback saved in: {img_path}")
        print(f"🔍 Extracted hidden message: {extracted_msg}")

        logs.append({
            "item": item,
            "final_action": classification["action"],
            "confidence": classification["confidence"],
            "reason": classification["reason"],
            "feedback_status": feedback_result["status"],
            "hidden_image": img_path,
            "hidden_data_verified": extracted_msg
        })

    with open("logs/actions.json", "w") as f:
        json.dump(logs, f, indent=4)

    print("\n✅ Processing completed! Check logs/actions.json and outputs/ for PNGs.")



from cognitive_modules.stego_handler import StegoHandler

stego = StegoHandler()
msg = stego.extract_message("outputs/hidden_feedback_1.png")
print("Extracted hidden message:", msg)

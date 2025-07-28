class FeedbackHandler:
    def __init__(self, classifier):
        self.classifier = classifier

    def apply_feedback(self, old_action, new_action):
        self.classifier.update_weights(old_action, new_action)
        status = "Confirmed 👍" if old_action == new_action else "Updated 👎"
        return status

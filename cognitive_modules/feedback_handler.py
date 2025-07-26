class FeedbackHandler:
    VALID_ACTIONS = ["Reply", "Tag", "Archive", "Add to Calendar", "Forward", "Later"]

    def get_feedback(self, predicted_action):
        user_input = input(
            f"Do you approve this action '{predicted_action}'? (y/n or type new action): "
        ).strip().lower()

        if user_input in ["y", "yes"]:
            return {"status": "approved", "new_action": predicted_action}
        elif user_input in ["n", "no"]:
            new_action = input(f"Enter the correct action ({'/'.join(self.VALID_ACTIONS)}): ").strip()
            if new_action in self.VALID_ACTIONS:
                return {"status": "overridden", "new_action": new_action}
            else:
                print("❌ Invalid action entered. Keeping predicted action.")
                return {"status": "approved", "new_action": predicted_action}
        elif user_input in [a.lower() for a in self.VALID_ACTIONS]:
            return {"status": "overridden", "new_action": user_input.title()}
        else:
            print("❌ Invalid input. Keeping predicted action.")
            return {"status": "approved", "new_action": predicted_action}



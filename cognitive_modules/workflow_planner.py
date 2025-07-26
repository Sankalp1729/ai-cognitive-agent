class WorkflowPlanner:
    def plan(self, classification):
        primary_action = classification["action"]
        workflow = [primary_action]

        if primary_action == "Forward":
            workflow.append("Add Note")
        elif primary_action == "Add to Calendar":
            workflow.append("Tag")

        return workflow

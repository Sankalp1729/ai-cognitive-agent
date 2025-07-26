class EmailProcessor:
    def parse_email(self, email_data):
        return email_data.get("subject", "") + " " + email_data.get("body", "")

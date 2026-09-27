class ConversationState:
    def __init__(self, customer_name=None, company_name=None, requirement=None):
        self.customer_name = customer_name
        self.company_name = company_name
        self.requirement = requirement

        self.capacity = None
        self.location = None
        self.application = None
        self.budget = None
        self.timeline = None

    def to_dict(self):
        return {
            "customer_name": self.customer_name,
            "company_name": self.company_name,
            "requirement": self.requirement,
            "capacity": self.capacity,
            "location": self.location,
            "application": self.application,
            "budget": self.budget,
            "timeline": self.timeline
        }
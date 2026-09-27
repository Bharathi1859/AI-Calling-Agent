from app.database import Base, engine

from app.models.customer import Customer
from app.models.call import Call
from app.models.conversation import ConversationMessage
from app.models.summary import CallSummary


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
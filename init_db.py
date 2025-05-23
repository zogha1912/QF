from databse.database import Base, engine
from models import models

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
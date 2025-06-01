from sqlalchemy import create_engine, text

# Create engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/tamp_vehicle')

# Test connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Connection successful!") 
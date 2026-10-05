from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Create a local SQLite database file named campus_seats.db
DATABASE_URL = "sqlite:///./campus_seats.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Define the Seat Table structure
class DepartmentSeat(Base):
    __tablename__ = "department_seats"

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(String, unique=True, index=True)
    department_name = Column(String)
    total_seats = Column(Integer)
    available_seats = Column(Integer)

# 3. Create tables and add initial sample data
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Only add sample data if the table is empty
    if db.query(DepartmentSeat).count() == 0:
        initial_data = [
            DepartmentSeat(department_code="CSE", department_name="Computer Science & Engineering", total_seats=120, available_seats=14),
            DepartmentSeat(department_code="AI-DS", department_name="Artificial Intelligence & Data Science", total_seats=60, available_seats=5),
            DepartmentSeat(department_code="ECE", department_name="Electronics & Communication Engineering", total_seats=90, available_seats=28),
            DepartmentSeat(department_code="MECH", department_name="Mechanical Engineering", total_seats=60, available_seats=0),
        ]
        db.add_all(initial_data)
        db.commit()
        print("Success: Database created and filled with sample departments!")
    else:
        print("Database already exists.")
    
    db.close()

if __name__ == "__main__":
    setup_database()
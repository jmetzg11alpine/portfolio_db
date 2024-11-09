from database import SessionLocal, Base, engine
from get_budget import BudgetCSV
from update import AddGovSpending
import sys

Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'get':
        BudgetCSV(2024, list(range(2017, 2025))).get_data()

    elif len(sys.argv) > 1 and sys.argv[1] == 'update':
        session = SessionLocal()
        try:
            AddGovSpending(session)
        finally:
            session.close()

    else:
        print('add argument: update_budget')

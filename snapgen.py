from models.dbcontext import DbContext as db
from models.db.student import Student

def main():
    """
    (re)generates all student snapshots;
    meant to run as a batch process
    """
    with db.session_scope() as session:
        Student.generate_all_snapshots(session)

main()

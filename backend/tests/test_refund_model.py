from config.database import SessionLocal
from models.refund import Refund
from services.refund import check_refund_eligibility

with SessionLocal() as session:

    refunds = session.query(Refund).all()

    print("Refund records:", refunds)

print(
    check_refund_eligibility("ORD-TEST-001")
)

print(
    check_refund_eligibility("ORD-DOES-NOT-EXIST")
)
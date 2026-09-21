from services.refund import check_refund_eligibility

from services.refund import refund_workflow

print(
    check_refund_eligibility("ORD-1001")
)

print(
    check_refund_eligibility("ORD-1003")
)

print(
    check_refund_eligibility("ORD-1004")
)

print(
    check_refund_eligibility("ORD-9999")
)



print(refund_workflow("ORD-1001"))

print(refund_workflow("ORD-1003"))

print(refund_workflow("ORD-1004"))
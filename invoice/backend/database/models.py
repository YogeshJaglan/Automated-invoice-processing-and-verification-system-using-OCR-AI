from sqlalchemy import Column, Integer, String, Float, JSON
from .db import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String)
    gstin = Column(String)
    invoice_number = Column(String)
    invoice_date = Column(String)
    total_amount = Column(Float)
    tax_data = Column(JSON)
    status = Column(String)
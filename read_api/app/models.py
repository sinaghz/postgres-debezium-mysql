from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(String)
    status = Column(String)
    date_created = Column(String)

    shipments = relationship("Shipment", back_populates="order")


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(String)
    status = Column(String)
    order_id = Column(Integer, ForeignKey("orders.id"))

    order = relationship("Order", back_populates="shipments")




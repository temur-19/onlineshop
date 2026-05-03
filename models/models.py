from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Integer, String, ForeignKey, Numeric
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(100),nullable=False)
    email: Mapped[str] = mapped_column(String(100),nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100),nullable=False)
    role: Mapped[str] = mapped_column(String(50),nullable=False,default='xaridor')
    products: Mapped[list["Product"]] = relationship("Product", back_populates="customer",cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="user")
    balance: Mapped["Balance"] = relationship("Balance", back_populates="user", uselist=False)

class Product(BaseModel):
    __tablename__ = "products"
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    description: Mapped[str] = mapped_column(String(255),nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2),nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    customer: Mapped["User"] = relationship("User", back_populates="products")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="product")

class Order(BaseModel):
    __tablename__ = "orders"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="orders")
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
    payment: Mapped["Payment"] = relationship("Payment", back_populates="order", uselist=False)

class Payment(BaseModel):
    __tablename__ = "payments"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    order: Mapped["Order"] = relationship("Order", back_populates="payment")
    user: Mapped["User"] = relationship("User", back_populates="payments")

class Balance(BaseModel):
    __tablename__ = "balances"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="balance")
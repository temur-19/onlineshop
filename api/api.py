import jwt
import asyncio
import security

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks
from fastapi.security import OAuth2userizationCodeBearer, OAuth2PasswordRequestForm
from typing import List

from schemas.schemas import  UserCreate, UserOut, ProductCreate, ProductOut, OrderCreate, OrderOut, PaymentCreate, PaymentOut
from models.models import User, Product, Order, Payment
from db.db import get_async_session, engine, get_db

api_router = APIRouter(prefix="/api", tags=["users"])
oauth2_schema = OAuth2userizationCodeBearer(userizationUrl="/users/login", tokenUrl="/users/login")

async def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNuserIZED,
        detail="Token yaroqsiz yoki muddati t   ugagan"
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = await db.scalar(select(User).where(User.id == int(user_id)))
    if user is None:
        raise credentials_exception

    return user


@api_router.post("/register/", response_model=UserOut)
async def register(user: UserCreate, db: Session = Depends(get_async_session)):
    hashed_password = security.get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@api_router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_async_session)):
    user = await db.scalar(select(User).where(User.email == form_data.username))
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNuserIZED, detail="Noto'g'ri email yoki parol")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}  

@api_router.post('/user_me/', response_model=UserOut)
async def get_currently_logged_in_user(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.post("/products/", response_model=ProductOut)
async def create_product(product: ProductCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)):
    new_product = Product(name=product.name, description=product.description, price=product.price, user_id=current_user.id)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product
@api_router.post("/orders/", response_model=OrderOut)
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)):
    new_order = Order(user_id=current_user.id, product_id=order.product_id, quantity=order.quantity)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order
@api_router.post("/payments/", response_model=PaymentOut)
async def create_payment(payment: PaymentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)):
    new_payment = Payment(order_id=payment.order_id, user_id=current_user.id, amount=payment.amount)
    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)
    return new_payment
@api_router.get("/orders/", response_model=List[OrderOut])
async def get_user_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)) -> List[OrderOut]:
    orders = await db.execute(select(Order).where(Order.user_id == current_user.id))
    return orders.scalars().all()

@api_router.get("/payments/", response_model=List[PaymentOut])
async def get_user_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)) -> List[PaymentOut]:
    payments = await db.execute(select(Payment).where(Payment.user_id == current_user.id))
    return payments.scalars().all()

@api_router.get("/products/", response_model=List[ProductOut])
async def get_user_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)) -> List[ProductOut]:
    products = await db.execute(select(Product).where(Product.user_id == current_user.id))
    return products.scalars().all()


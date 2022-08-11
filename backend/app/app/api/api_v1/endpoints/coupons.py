from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Coupon])
def read_coupons(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve coupons.
    """

    coupons = crud.coupon.get_multi(db, skip=skip, limit=limit)

    return coupons


@router.get("/assign", response_model=List[schemas.CouponAssigned])
def read_coupons_assign(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve coupon assigned.
    """
    if crud.user.is_superuser(current_user):
        coupon_assign = crud.couponassigned.get_multi(db, skip=skip, limit=limit)
    else:
        coupon_assign = crud.couponassigned.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return coupon_assign


@router.post("/", response_model=schemas.Coupon)
def create_coupon(
    *,
    db: Session = Depends(deps.get_db),
    coupon_in: schemas.CouponCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new coupon.
    """
    coupon = crud.coupon.create(db=db, obj_in=coupon_in)
    return coupon


@router.put("/{id}", response_model=schemas.Coupon)
def update_coupon(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    coupon_in: schemas.CouponUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an coupon.
    """
    coupon = crud.coupon.get(db=db, id=id)
    if not coupon:
        raise HTTPException(status_code=404, detail="coupon not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    coupon = crud.coupon.update(db=db, db_obj=coupon, obj_in=coupon_in)
    return coupon

@router.post("/assign/{id_coupon}", response_model=schemas.CouponAssigned)
def assign_coupon(
    *,
    db: Session = Depends(deps.get_db),
    id_coupon: int,
    current_user: models.User = Depends(deps.get_current_active_user), 
) -> Any:
    """
    Assign an coupon.
    """
    coupon = crud.coupon.get(db=db, id=id_coupon)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    # validar la cantidad del cupon

    count = crud.couponassigned.count_by_coupon(db=db, coupon_id=coupon.id)

    if count + 1 > coupon.quantity:
        raise HTTPException(status_code=404, detail="Coupon not found")


    # validar si el usuario ya tiene un cupon asignado
    userbycoupon = crud.couponassigned.get_by_owner_and_coupon(db=db, owner_id=current_user.id, coupon_id=coupon.id)

    if userbycoupon:
        raise HTTPException(status_code=404, detail="An user can't have two coupons of the same offer") 


    couponassign_in = schemas.CouponAssignedCreate(
        owner_id = current_user.id,
        coupon_id = coupon.id
    )

    couponassign = crud.couponassigned.create(db=db, obj_in=couponassign_in)
    return couponassign


@router.put("/redeem/{owner_id}/{coupon_id}", response_model=schemas.CouponAssigned)
def redeem_coupon(
    *,
    db: Session = Depends(deps.get_db),
    owner_id: int,
    coupon_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Redeem an coupon.
    """
    coupon = crud.couponassigned.get_by_owner_and_coupon(db=db, owner_id=owner_id, coupon_id=coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    if not crud.user.is_superuser(current_user) and (coupon.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if coupon.redeemed:
        raise HTTPException(status_code=400, detail="The coupon has been redeemed")

    couponassign_in = schemas.CouponAssignedUpdate(
        owner_id = coupon.owner_id,
        coupon_id = coupon.coupon_id,
        redeemed = True
    )

    couponassigned = crud.couponassigned.update(db=db, db_obj=coupon, obj_in=couponassign_in)
    return couponassigned


@router.get("/{id}", response_model=schemas.Coupon)
def read_coupon(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get coupon by ID.
    """
    coupon = crud.coupon.get(db=db, id=id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon


@router.get("/assign/{owner_id}/{coupon_id}", response_model=schemas.CouponAssigned)
def read_coupon_assign(
    *,
    db: Session = Depends(deps.get_db),
    owner_id: int,
    coupon_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get coupon assign by ID.
    """
    coupon = crud.couponassigned.get_by_owner_and_coupon(db=db, owner_id=owner_id, coupon_id=coupon_id)
    if coupon.redeemed:
        raise HTTPException(status_code=404, detail="Coupon redeemed")
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    if not crud.user.is_superuser(current_user) and (coupon.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return coupon

# @router.delete("/{id}", response_model=schemas.Item)
# def delete_coupon(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an item.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.item.remove(db=db, id=id)
#     return item

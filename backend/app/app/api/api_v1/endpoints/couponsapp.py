from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from app import crud, models, schemas 
from app.api import deps
from datetime import datetime, timedelta
from app.utils import save_image, create_excel


router = APIRouter()
formats = [".png", ".jpg"]

#get by owner id
@router.get("/", response_model=List[schemas.CuponInDBBase])
def read_coupons(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    owner_id: int = None,
    category_id: int = None
) -> Any:
    """
    Retrieve coupons.
    """
    if owner_id:
        coupons = crud.coupon.get_all_by_owner(db, owner_id=owner_id, skip=skip, limit=limit)
    elif category_id:
        coupons = crud.coupon.get_all_to_user_by_category(db, category_id=category_id, skip=skip, limit=limit)
    else:
        coupons = crud.coupon.get_all_to_user(db, skip=skip, limit=limit)
    return coupons

#create coupon
@router.post("/", response_model=schemas.CuponInDBBase)
def create_coupon(
    *,
    db: Session = Depends(deps.get_db),
    coupon_in: schemas.CuponCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new coupon.
    """
    coupon_in.owner_id = current_user.id
    coupon = crud.coupon.create(db=db, obj_in=coupon_in)
    return coupon

#set image to coupon
@router.patch("/{id}/image", response_model=schemas.CuponInDBBase)
async def upload_coupon(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_superuser)
    ) -> Any:
    """
    Update image of coupon.
    """
    coupon = crud.coupon.get(db=db, id=id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    if coupon.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    coupon.img = save_image(formats,"coupons",file)
    db.commit()
    db.refresh(coupon)
    return coupon

#update coupon and validate owner
@router.put("/{id}", response_model=schemas.CuponInDBBase)
def update_coupon(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    coupon_in: schemas.CuponUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an coupon.
    """
    coupon = crud.coupon.get(db=db, id=id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")   
    if coupon.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    coupon = crud.coupon.update_with_owner(db=db, db_obj=coupon, obj_in=coupon_in)
    return coupon

#delete coupon and validate owner
@router.delete("/{id}", response_model=dict)
def delete_coupon(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> dict:
    """
    Delete a coupon.
    """
    coupon = crud.coupon.get(db=db, id=id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    if coupon.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    # Elimina el cupón
    crud.coupon.remove(db=db, id=id)

    # Devuelve un mensaje indicando que se ha eliminado el cupón
    return {"message": f"Coupon with ID {id} has been deleted"}


####### CATEGORIES #######
#get all categories
@router.get("/category", response_model=List[schemas.CuponCategoryInDBBase])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve categories.
    """
    categories = crud.coupon.get_all_categories(db, skip=skip, limit=limit)
    return categories

#create category
@router.post("/category", response_model=schemas.CuponCategoryInDBBase)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CuponCategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new category.
    """
    category_in.created_by = current_user.id
    category_in.updated_by = current_user.id
    category = crud.category.create(db=db, obj_in=category_in)
    return category

#set image to category
@router.patch("/category/{id}/image", response_model=schemas.CuponCategoryInDBBase)
async def upload_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_superuser)
    ) -> Any:
    """
    Update image of category.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.created_by != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    category.img = save_image(formats,"couponCategories",file)
    db.commit()
    db.refresh(category)
    return category

#update category and validate owner
@router.put("/category/{id}", response_model=schemas.CuponCategoryInDBBase)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    category_in: schemas.CuponCategoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an category.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")   
    if category.created_by != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    category_in.updated_by = current_user.id
    category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    return category

#delete category and validate owner
@router.delete("/category/{id}", response_model=dict)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> dict:
    """
    Delete a category.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.created_by != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    # Elimina el cupón
    crud.category.remove(db=db, id=id)

    # Devuelve un mensaje indicando que se ha eliminado el cupón
    return {"message": f"Category with ID {id} has been deleted"}


####### COUPON ASSIGNED #######
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

    now = datetime.utcnow()
    coupon = crud.coupon.get(db=db, id=id_coupon)
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    #start validar fecha de inicio
    if coupon.start:
        raise HTTPException(status_code=404, detail="Coupon not started")

    # si la fecha de expiracion es mayor al tiempo actual
    if (coupon.expiration_date < now):
        raise HTTPException(status_code=404, detail="Time expiration")

    # validar la cantidad del cupon

    count = crud.couponassigned.count_by_coupon(db=db, coupon_id=coupon.id)

    if count + 1 > coupon.quantity:
        raise HTTPException(status_code=404, detail="Coupon not found")

    # validar que el ultimo cupon asignado ya haya pasado el tiempo de espera
    last = crud.couponassigned.get_last_by_coupon(db=db, coupon_id=coupon.id)

    if last:
        # now = datetime.utcnow()

        if (last.created_at + timedelta(minutes=int(coupon.time))) > now:
            raise HTTPException(status_code=404, detail="Lock by time")

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

####### COUPON REDEEMED #######
#redeem coupon and response message
@router.post("/redeem", response_model=dict)
def redeem_coupon(
    *,
    db: Session = Depends(deps.get_db),
    coupon_in: schemas.CouponReedeemedCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Redeem an coupon.
    """
    crud.redeemed.redeem_coupon(db=db, obj_in=coupon_in)


####### COUPON REPORT #######
#download report of coupons
@router.get("/report")
def download_report(
    db: Session = Depends(deps.get_db),
    owner_id: int = None,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Download report of coupons.
    """
    try:
        # Obtén los datos del informe desde la base de datos
        report_data = crud.coupon.get_report(db=db, owner_id=owner_id)
        print(report_data)
        # Crea el archivo Excel
        xls = create_excel(report_data)

        # Configura los encabezados para la descarga del archivo
        response = StreamingResponse(
            iter([xls.getvalue()]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response.headers["Content-Disposition"] = 'attachment; filename="reporte.xlsx"'

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}",
        )
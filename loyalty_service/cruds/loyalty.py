from models.loyalty import LoyaltyModel
from schemas.loyalty import LoyaltyUpdate
from cruds.interfaces.loyalty import ILoyaltyCRUD


class LoyaltyCRUD(ILoyaltyCRUD):
    async def get_all(self, offset: int = 0, limit: int = 100):
        return self._db.query(LoyaltyModel).offset(offset).limit(limit).all()

    async def get_by_id(self, loyalty_id: int):
        return self._db.query(LoyaltyModel).filter(LoyaltyModel.id == loyalty_id).first()
    
    async def get_by_username(self, user_name: str):
        return self._db.query(LoyaltyModel).filter(LoyaltyModel.username == user_name).first()

    async def add(self, loyalty: LoyaltyModel):
        try:
            self._db.add(loyalty)
            self._db.commit()
            self._db.refresh(loyalty)
        except:
            return None
        
        return loyalty
    
    async def delete(self, loyalty: LoyaltyModel):
        self._db.delete(loyalty)
        self._db.commit()
        
        return loyalty

    async def patch(self, loyalty: LoyaltyModel, loyalty_update: LoyaltyUpdate):
        update_attributes = loyalty_update.model_dump(exclude_unset=True)        

        for key, value in update_attributes.items():
            setattr(loyalty, key, value)
        
        try:
            self._db.add(loyalty)
            self._db.commit()
            self._db.refresh(loyalty)
        except:
            return None
        
        return loyalty

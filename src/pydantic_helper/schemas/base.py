from pydantic import BaseModel


class BaseSchema(BaseModel):
    
    
    def to_dict(
        self,
        exclude_fields: list[str] = [],
        include_fields: dict = {},
        exclude_none: bool = False,
    ) -> dict:
        
        data = self.model_dump()
        
        data = {k: v for k, v in data.items() if k not in exclude_fields and (not exclude_none or v is not None)}
        
        data.update(include_fields)
        
        return data
        
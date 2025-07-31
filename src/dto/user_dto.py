from pydantic import BaseModel
from typing import Optional

class UserDTO(BaseModel):
    username: str
    email: str
    phone_number: Optional[str] = None
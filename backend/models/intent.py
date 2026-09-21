from typing import Optional

from pydantic import BaseModel


class UserIntent(BaseModel):

    intent: str

    order_id: Optional[str] = None
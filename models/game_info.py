from typing import TypedDict, Optional

class GameInfo(TypedDict):
    title: str
    link: str
    discount: str
    price: float
    image_url: Optional[str]
    image_path: Optional[str]
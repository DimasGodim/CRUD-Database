from pydantic import BaseModel, Field

class modelNFT(BaseModel):
    judul: str
    dekripsi: str
    harga: float

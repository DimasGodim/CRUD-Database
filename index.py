from fastapi import FastAPI, Request, File, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel

from connector import(
    SQL,
    MONGGO
)
from helper import(
    get_data,
    image_confirmation
)

class modelNFT(BaseModel):
    judul: str
    dekripsi: str
    harga: float

app = FastAPI()


@app.get("/get-all-data")
async def get_data(): 
    asset = MONGGO()
    SQL = SQL()
    perintah = SQL.cursor()

    perintah.execute("SELECT id, judul, deskripsi, harga FROM asset")
    hasil = perintah.fetchall()
    id_data = id in hasil
    data =  get_data(perintah, id_data)
    return JSONResponse(content=json.dumps({"hasil": data}))   

@app.post("/post-data")
async def make_new_data(model: modelNFT, nft_file: UploadFile = File(...)):
    data = json.dumps(model)

    asset = MONGGO()
    db = SQL()
    perintah = db.cursor()

    with open(f"temp/{nft_file.filename}", "wb") as f:
        f.write(await nft_file.read())
    if not image_confirmation(f"temp/{nft_file.filename}"):
        os.remove(f"temp/{nft_file.filename}")
        raise HTTPException(status_code=400, detail="File yang diunggah bukan file gambar.")
    with open(f"temp/{nft_file.filename}", "rb") as f:
        image_data = f.read()

    perintah.execute("INSERT INTO asset (judul, deskripsi, harga) VALUES (%s, %s, %s)",
    (data.judul, data.dekripsi, data.harga))

    db.commit()
    
    id_data = perintah.lastrowid
    asset.insert_one({"_id": id_data, "main": image_data})
    data_get = get_data(perintah, id_data)
    os.remove(f"temp/{nft_file.filename}")

    return JSONResponse(content=json.dumps({"hasil": data_get}))

@app.get("/search-data/{judul}")
async def search_data(judul: str):
    asset = MONGGO()
    SQL = SQL()
    perintah = SQL.cursor()

    perintah.execute(f"SELECT id, judul, deskripsi, harga FROM asset WHERE judul = {judul}")
    hasil = perintah.fetchall()
    id_data = id in hasil
    data = get_data(perintah, id_data)
    return JSONResponse(content=json.dumps({"hasil": data}))

@app.put("/all-update-data/{id_data}")
async def update_data(id_data: str, data: modelNFT):
    asset = MONGGO()
    SQL = SQL()
    perintah = SQL.cursor()

    perintah.execute(f"UPDATE asset set judul = {data.judul}, deskripsi = {data.dekripsi}, harga = {data.harga} WHERE id = {id_data}")
    SQL.commit()
    data = get_data(perintah, id_data)
    return JSONResponse(content=json.dumps({"update": data}))

@app.delete("/delete-data/{id_data}")
async def delete_data(id_data: str):
    asset = MONGGO()
    SQL = SQL()
    perintah = SQL.cursor()

    data = get_data(perintah, id_data)
    perintah.execute(f"DELETE FROM asset WHERE id = {id_data}")
    SQL.commit()
    return JSONResponse(content=json.dumps({"delete": data}))

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_msg = f"Error occurred: {str(exc)}"
    return JSONResponse(status_code=500, content={"message": error_msg})    
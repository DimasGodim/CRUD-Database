from PIL import Image

def get_data(perintah, id_data):
    perintah.execute(f"SELECT id, judul, deskripsi, harga FROM asset WHERE id = {id_data}")
    hasil = perintah.fetchall()
    dic= []
    for row in hasil: 
        id = row[0]
        judul = row[1]
        deskripsi = row[2]
        harga = row [3]
    dic.append({"id": id, "judul": judul, "deskripsi": deskripsi, "harga": harga})    
    return dic

def image_confirmation(file_path):
    try:
        Image.open(file_path)
        return True
    except:
        return False

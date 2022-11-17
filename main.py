from fastapi import FastAPI, Form
import psycopg2
import os
import dotenv

dotenv.load_dotenv()

class Canil:
    def __init__(self):
        self.conexao = psycopg2.connect(user=os.environ['FDB_user'],
                                  password=os.environ['FDB_password'],
                                  host=os.environ['FDB_host'],
                                  port=os.environ['FDB_port'],
                                  database=os.environ['FDB_database'])
        self.cursor = self.conexao.cursor()


    def selectfull(self):
        self.cursor.execute("SELECT * FROM ANIMAIS")
        return self.cursor.fetchall()

    def selectwhere(self,id):
        self.cursor.execute(f"SELECT * FROM ANIMAIS WHERE ID = {id}")
        return self.cursor.fetchall()

    def delete(self,id):
        self.cursor.execute(f"DELETE FROM ANIMAIS WHERE ID = {id}")
        self.conexao.commit()

    def insertclient(self,username,email,number,password):
        self.cursor.execute("INSERT INTO CLIENTES(nome,email,senha,telefone) VALUES('{username}','{email}',{number},'{password}')")
        self.conexao.commit()

    def insertanimal(self,especie,raca,vac,cast,age):
        self.cursor.execute("INSERT INTO ANIMAIS(especie,raca,vacinado,castrado,idade) VALUES('{especie}','{raca}',{vacinado},{castrado},{idade})")
        self.conexao.commit()

canil = Canil()
app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(), email: str = Form(), number: int = Form() ,password: str = Form()):
    canil.insertclient(username,email,number,password)
    return {"username": username}
    

@app.get("/animais")
def animais():
    return canil.selectfull()

    
@app.get("/animais/{id}")
def animal(id: int):
    return canil.selectwhere(id)


@app.post("/cadanimal/")
async def cadanimal(especie: str = Form(), raca : str = Form(), vac: bool = Form(), cast: bool = Form(), age: int = Form()):
    canil.insertanimal(especie,raca,vac,cast,age)
    return {"especie": especie}



@app.get("/delanimal/{id}")
def delete(id: int):
    return canil.delete(id)
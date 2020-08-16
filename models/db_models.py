from sqlalchemy import Integer, String, Numeric, Column, Sequence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Declarando nova base
base = declarative_base()

class Produtos(base):

    __tablename__ = 'produtos'
    produto_id = Column(Integer, Sequence('produto_id', start=1), 
                        primary_key=True)
    nome = Column(String(50))
    preco = Column(Numeric)
    descricao = Column(String)


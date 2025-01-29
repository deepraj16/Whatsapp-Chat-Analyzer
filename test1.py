import pandas as pd 
import preprocesser 
path='WhatsApp Chat with GD.txt'
f=open(path,'r',encoding='utf-8')
data =f.read()

k=preprocesser.preprocessor(data)
print(type(k))
print(len(k))
print(k.sample(4))

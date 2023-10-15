#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('2021-01.csv')
df['Fecha_Retiro_alt']=pd.to_datetime(df['Fecha_Retiro'],format='%d/%m/%Y')
df['Tiempo_Arribo']=pd.to_datetime(df['Fecha_Arribo']+' '+df['Hora_Arribo'],format='%d/%m/%Y %H:%M:%S')
df['Tiempo_Retiro']=pd.to_datetime(df['Fecha_Retiro']+' '+df['Hora_Retiro'])  

## Arreglar errores del formateo y limpieza de datos.


for j in range(1,10):
    df1=df.set_index('Tiempo_Arribo')
    df2=df.reset_index().set_index('Tiempo_Arribo').loc['2021-01-0{}'.format(j)]
    mm=df2.loc['2021-01-0{}'.format(j),'Tiempo_Retiro'].tolist()
    for i in range(0,len(mm)):
        mm[i]=mm[i].replace(month=1,day=j)

    inter=pd.DataFrame(mm)
    inter['Tiempo_Arribo']=df2.loc['2021-01-0{}'.format(j),'Tiempo_Retiro'].index
    inter=inter.rename(columns={0:'Tiempo_Retiro'}).set_index('Tiempo_Arribo')

    df2.loc['2021-01-0{}'.format(j),'Tiempo_Retiro']=inter
    df1.loc['2021-01-0{}'.format(j)]=df2
    df=df1.reset_index()

for j in range(10,32):
    df1=df.set_index('Tiempo_Arribo')
    df2=df.reset_index().set_index('Tiempo_Arribo').loc['2021-01-{}'.format(j)]
    mm=df2.loc['2021-01-{}'.format(j),'Tiempo_Retiro'].tolist()
    for i in range(0,len(mm)):
        mm[i]=mm[i].replace(month=1,day=j)

    inter=pd.DataFrame(mm)
    inter['Tiempo_Arribo']=df2.loc['2021-01-{}'.format(j),'Tiempo_Retiro'].index
    inter=inter.rename(columns={0:'Tiempo_Retiro'}).set_index('Tiempo_Arribo')

    df2.loc['2021-01-{}'.format(j),'Tiempo_Retiro']=inter
    df1.loc['2021-01-{}'.format(j)]=df2
    df=df1.reset_index()


##


df['Tiempo_Minutos']=(df.Tiempo_Arribo-df.Tiempo_Retiro)/pd.Timedelta(minutes=1)
df=df[['Tiempo_Retiro','Tiempo_Arribo','Tiempo_Minutos','Bici','Fecha_Retiro_alt']]

dfnuevo=df.drop(index=df[df['Tiempo_Minutos']<0].index)
dfnuevo.set_index('Fecha_Retiro_alt',inplace=True)

dfnuevo.groupby(dfnuevo.index).mean()

fig, ax = plt.subplots();
xticks=[i for i in range(1,32)]
ax.scatter(xticks,dfnuevo.groupby(dfnuevo.index).mean().loc['2021-01-01':].Tiempo_Minutos);
ax.legend(['Tiempo promedio de viaje'],loc='upper left');
fig.suptitle('Tiempo de viaje promedio por día en enero');

plt.savefig("time series avg trip length 2022 01.png")
dfnuevo['Tiempo_Minutos'].to_csv('time series avg trip length 2022 01.csv')


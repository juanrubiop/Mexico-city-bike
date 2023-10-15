#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('2021-01.csv')
df['Fecha_Retiro']= pd.to_datetime(df['Fecha_Retiro'],format='%d/%m/%Y')
df['Fecha_Arribo']= pd.to_datetime(df['Fecha_Arribo'],format='%d/%m/%Y')

#271
datosEstacionArribo=df[['Ciclo_Estacion_Arribo','Fecha_Arribo']]
datosEstacionArribo=datosEstacionArribo[datosEstacionArribo['Ciclo_Estacion_Arribo']==271]

datosEstacionRetiro=df[['Ciclo_Estacion_Retiro','Fecha_Retiro']]
datosEstacionRetiro=datosEstacionRetiro[datosEstacionRetiro['Ciclo_Estacion_Retiro']==271]

datosEstacionRetiro=datosEstacionRetiro.set_index('Fecha_Retiro')
datosEstacionArribo=datosEstacionArribo.set_index('Fecha_Arribo')

datosEstacionRetiro=datosEstacionRetiro.groupby(datosEstacionRetiro.index.date).count()
datosEstacionArribo=datosEstacionArribo.groupby(datosEstacionArribo.index.date).count()

fig, ax = plt.subplots()
xticks=[i for i in range(1,32)]
ax.scatter(xticks,datosEstacionRetiro.Ciclo_Estacion_Retiro)
ax.scatter(xticks,datosEstacionArribo.Ciclo_Estacion_Arribo)
ax.legend(['Retiros estación 271','Arribos estación 271']);
fig.suptitle('Arribos y retiros de la estación más concurrida en enero');

datosEstacionArribo['Ciclo_Estacion_Retiro']=datosEstacionRetiro['Ciclo_Estacion_Retiro']


plt.savefig("time series top station 2022 01.png")
datosEstacionArribo.to_csv('time series top station 2022 01.csv')


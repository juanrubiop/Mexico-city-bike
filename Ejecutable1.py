#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('2021-01.csv')
df['Fecha_Retiro']= pd.to_datetime(df['Fecha_Retiro'],format='%d/%m/%Y')
df['Fecha_Arribo']= pd.to_datetime(df['Fecha_Arribo'],format='%d/%m/%Y')
df.head()
retiros=df[['Fecha_Retiro','Ciclo_Estacion_Retiro']].set_index('Fecha_Retiro')
retiros=retiros.groupby(retiros.index.date).count()
fig, ax = plt.subplots()
xticks=[30,31]
agregado=[i for i in range(1,32)]
xticks.extend(agregado)
ax.scatter(xticks,retiros.Ciclo_Estacion_Retiro)
ax.legend(['Retiros totales'])
fig.suptitle('Retiros totales por día en Enero')

plt.savefig('time series withdrawals 2022 01.png')
retiros.to_csv('time series withdrawals 2022 01.csv')


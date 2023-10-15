#!/usr/bin/env python
# coding: utf-8

# In[ ]:


df=pd.read_csv('2021-01.csv')
df['Fecha_Retiro_alt']=pd.to_datetime(df['Fecha_Retiro'],format='%d/%m/%Y')
df['Tiempo_Arribo']=pd.to_datetime(df['Fecha_Arribo']+' '+df['Hora_Arribo'],format='%d/%m/%Y %H:%M:%S')
df['Tiempo_Retiro']=pd.to_datetime(df['Fecha_Retiro']+' '+df['Hora_Retiro'])  

## Arreglar errores del formateo


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

for j in range(10,13):
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



bici=df

bici['Tiempo_Horas']=(bici.Tiempo_Arribo-bici.Tiempo_Retiro)/pd.Timedelta(hours=1)
bici=bici.drop(index=bici[bici['Tiempo_Horas']<0].index)


viajesTotales=[len(bici[bici['Bici']==i]) for i in np.unique(bici.Bici)]
usuariosHombres=bici[(bici['Genero_Usuario']=='M')].set_index('Bici')
usuariosMujeres=bici[(bici['Genero_Usuario']=='F')].set_index('Bici')
usuariosHombres=usuariosHombres.groupby(usuariosHombres.index).count()['Genero_Usuario']
usuariosMujeres=usuariosMujeres.groupby(usuariosMujeres.index).count()['Genero_Usuario']
median=bici[['Edad_Usuario','Bici']].set_index('Bici')
median=median.groupby(median.index).median()['Edad_Usuario']
maxima=bici[['Edad_Usuario','Bici']].set_index('Bici')
maxima=maxima.groupby(maxima.index).max()['Edad_Usuario']
totHoras=bici[['Tiempo_Horas','Bici']].set_index('Bici')
totHoras=totHoras.groupby(totHoras.index).sum()['Tiempo_Horas']
promHoras=bici[['Tiempo_Horas','Bici']].set_index('Bici')
promHoras=promHoras.groupby(promHoras.index).mean()['Tiempo_Horas']
stdHoras=bici[['Tiempo_Horas','Bici']].set_index('Bici')
stdHoras=stdHoras.groupby(stdHoras.index).std()['Tiempo_Horas']

infoBici=pd.DataFrame(viajesTotales)
infoBici.rename(columns={0:'Viajes'},inplace=True)
infoBici['Bici']=np.unique(bici.Bici)
infoBici.dropna(inplace=True)
infoBici=infoBici.set_index('Bici')
infoBici['Viajes_Hombres']=usuariosHombres
infoBici['Viajes_Mujeres']=usuariosMujeres
infoBici['Mediana_Edad']=median
infoBici['Edad_Maxima']=maxima
infoBici['Total_Horas']=totHoras
infoBici['Promedio_de_Horas']=promHoras
infoBici['Desviación_Estandar_Horas']=stdHoras

infoBici.to_csv('bike_month_statistics.csv')
infoBici.head()


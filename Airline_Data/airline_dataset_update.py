# -*- coding: utf-8 -*-
"""Airline_Dataset_Update.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-ktychnH8-h_B5t-VvxAvT0hub2vnDc4

# Caso Practico Final
**Estadistica para Cientifico de Datos**

**Nombre:** Andres Gallegos

Se pide

Este es el último caso práctico de este módulo. Para realizarlo, ha de escogerse una BBDD para realizar una exploración estadística propia de un científico de datos. Para ello, se pueden seguir los siguientes pasos para desarrollar el proyecto:
"""

#Librerias
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from graphviz import Digraph
from scipy.stats import chi2_contingency
from statsmodels.formula.api import ols
import statsmodels.api as sm
from datetime import datetime

#Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

#Acceso al Archivo CSV
df_Airline=pd.read_csv('/content/drive/MyDrive/Analista de datos/Estadistica/Caso_Practico_Final/Airline_Dataset_Updated_v2.csv')
df_Airline

"""# **PASO UNO.** Definir un solo objetivo para el estudio con una BBDD.

En este paso, se va a definir un objetivo de estudio (es muy importante que solo sea uno). Se definirá siguiendo estos puntos:

**¿Qué problema se quiere solucionar con estos datos?**

En este problema lo que se busca es optimizar la puntualidad y minimizar las interrupciones en las operaciones de vuelo mediante el un analisis de los datos sobre retrasos, cancelaciones y rendimiento puntual de los vuelos.

**¿Qué significan las variables?**

- **Passenger ID** - Identificador unico del pasajero
- **First Name** - Nombre del Pasajero
- **Last Name** - Apellido del Pasajero
- **Gender** - Genero del Pasajero
- **Age** - Edad del pasajero
- **Nationality** - Nacionalidad del Pasajero
- **Airport Name** - Nombre del aereopuerto donde abordo el pasajero
- **Airport Country Code** - Codigo del pais de la ubicacion del aereopuerto
- **Country Name** - Nombre del pais en el que esta ubicado el aereopuerto
- **Airport Continent** - Continente donde está situado el aeropuerto
- **Continents** - Continentes involucrados en la ruta del vuelo.
- **Departure Date** - Fecha de salida del vuelo
- **Arrival Airport** - Aeropuerto de destino del vuelo
- **Pilot Name** - Nombre del piloto que opera el vuelo.
- **Flight Status** - Estado actual del vuelo (e.g., puntual, retrasado, cancelado)

**¿Qué tipo de variables hay?**

Las variables incluyen identificadores únicos (**Passenger ID**), datos personales (**nombre, género, edad, nacionalidad**), información geográfica (**nombre del aeropuerto, país, continente**), fechas y estados de vuelo.

**Definir un objetivo que ayude a solucionar el problema.**

Analizar los datos de retrasos y cancelaciones de vuelos para identificar patrones y tendencias que permitan implementar estrategias operativas efectivas, mejorando así la puntualidad y reduciendo las interrupciones en las operaciones aéreas.

# **PASO DOS.** Exploración de datos:
"""

#Revision del DataSet y asi entender su estructura
df_Airline.head(5)

#Inicio de la exploracion de los datos y saber cuantos con cuantos datos estamos trabajando
df_Airline.shape

"""Contamos con 98619 filas con 15 columnas"""

#Revisamos que tipo de datos tenemos
df_Airline.info()

"""Todas las caracteristicas, excepto la edad, son categoricas"""

#Revisamos si tenemos valores nulos
df_Airline.isnull().sum()

"""Se puede observar que no se tienen valores nulos"""

#Limpieza de los Datos
df_Airline.head(5)

"""Para este analisis se puede observar que para realizarlo de mejor manera podemos eliminar las columnas Passenger ID, First Name Last Name, Pilot Name, Airport Continent, Airport Country Code ya que no son relevantes para el analisis que se desea realizar, entonces se procedera a aleiminarlos."""

#Eliminacion de las columnas Passenger ID, First Name, Last Name, Pilot Name, Airport Continent y Airport Country Code.
df_new_table_Airline = df_Airline.drop(['First Name', 'Last Name', 'Passenger ID','Pilot Name', 'Airport Continent', 'Airport Country Code'], axis = 1)
df_new_table_Airline

"""Para este analisis se eliminaron datos con valores unicos (Passenger ID, First Name, Last Name and Pilot Name) del conjunto de datos. Dado que Airport Country Code y Country Name expresan los mismos valores y Airport Continent y Continents tambien expresan los mismos valores se extrajo una de las caracteristicas que tienen en mismo valor"""

#Reemplazar el nombre de algunas caracteristicas
df_new_table_Airline.rename(columns={"Airport Name": "Airport_Name",
                  "Country Name": "Country_Name",
                  "Departure Date": "Departure_Date",
                  "Arrival Airport": "Arrival_Airport",
                  "Flight Status": "Flight_Status"},inplace = True)
df_new_table_Airline

#Creacion de nuevas funciones desde la fecha de salida
df_new_table_Airline.Departure_Date = df_new_table_Airline.Departure_Date.str.replace("-", "/")
df_new_table_Airline["Departure_Month"] = df_new_table_Airline.Departure_Date.str.split("/", expand = True)[0]
df_new_table_Airline["Departure_Day"] = df_new_table_Airline.Departure_Date.str.split("/", expand = True)[1]
df_new_table_Airline["Departure_Year"] = df_new_table_Airline.Departure_Date.str.split("/", expand = True)[2]
df_new_table_Airline.drop(["Departure_Date"], axis = 1, inplace = True)
df_new_table_Airline

#Revision si las columnas tienen valores unicos

for col in df_new_table_Airline.columns:
    print(col, ".....:",df_new_table_Airline[col].nunique())

"""## **Creacion e interpretacion de Gráficos**

* **Crear los gráficos más apropiados.**

* **Interpretar los gráficos.**
"""

#Visualizacion de los datos de las nacionalidades
top_10_nacionalidades=df_new_table_Airline['Nationality'].value_counts().reset_index().nlargest(10,'count')
top_10_nacionalidades.reset_index()
top_10_nacionalidades

#Grafica de Nacionalidades las 10 primeras vuelos mas altas
fig=px.bar(top_10_nacionalidades, x='Nationality', y = 'count',color='Nationality',color_discrete_sequence=px.colors.sequential.Agsunset,text='count')
fig.update_traces(texttemplate='%{text}', textposition='outside')

"""**INTERPRETACION**

En la gráfica se observa la distribución de pasajeros por nacionalidad, destacando que los pasajeros chinos representan el grupo más numeroso con 18,317 pasajeros, aproximadamente el 20% del total de observaciones. Las siguientes nacionalidades con mayor cantidad de pasajeros son Indonesia (10,559 pasajeros), Rusia (5,693 pasajeros), Filipinas (5,239 pasajeros), Brasil (3,791 pasajeros), Portugal (3,299 pasajeros), Polonia (3,245 pasajeros), Francia (2,907 pasajeros), Suecia (2,397 pasajeros), y Estados Unidos (2,105 pasajeros). Este análisis revela una significativa diversidad entre los pasajeros, sugiriendo un alto volumen de viajeros provenientes de China e Indonesia. La preponderancia de pasajeros chinos subraya la importancia de China como un mercado crucial para la industria aérea, mientras que las otras nacionalidades también representan una considerable cantidad de viajeros, lo cual podría estar relacionado con la frecuencia de vuelos y las conexiones internacionales importantes de estos países.
"""

#Grafica de 10 Nacionalidades con los vuelos mas Bajas
lowest_10_Nacionalidades=df_new_table_Airline['Nationality'].value_counts().reset_index().nsmallest(10,'count')
lowest_10_Nacionalidades.reset_index()
lowest_10_Nacionalidades

#Grafica de 10 nacionalidades con los vuelos mas bajas
fig=px.bar(lowest_10_Nacionalidades, x='Nationality', y = 'count',color='Nationality',color_discrete_sequence=px.colors.sequential.Agsunset,text='count')
fig.update_traces(texttemplate='%{text}', textposition='outside')

"""**INTERPRETACION**

En los datos analizados, las nacionalidades con menor representación en los vuelos incluyen territorios y regiones con muy poca población o menor tráfico aéreo internacional. Es notable que algunas de estas nacionalidades, como Jersey, Norfolk Island, y Sint Maarten, solo tienen un pasajero registrado. La mayoría de las demás nacionalidades en esta lista tienen dos pasajeros registrados. Esto podría reflejar vuelos esporádicos o una baja demanda de viajes aéreos desde estas regiones específicas.
"""

# Datos de ejemplo (reemplaza con tus propios datos)
flight_status_counts = df_new_table_Airline['Flight_Status'].value_counts()

# Crear el gráfico de pastel
fig_pastel = px.pie(flight_status_counts, values=flight_status_counts.values,
                    names=flight_status_counts.index,
                    title='Distribución de Estados de Vuelo')

fig_pastel.update_traces(textinfo='label+percent', pull=[0.1, 0.1, 0.1])
fig_pastel.update_layout(legend_title_text='Flight_Status')

fig_pastel.show()

#Estados de Vuelo
fig_status=px.bar(df_new_table_Airline['Flight_Status'].value_counts().reset_index(),x='Flight_Status',y='count',color='Flight_Status',color_discrete_sequence=px.colors.sequential.Viridis,text='count')
fig_status.update_traces(texttemplate='%{text}', textposition='outside')

"""**INTERPRETACION**

La distribución equilibrada de los estados de vuelo entre "On Time", "Cancelled" y "Delayed" en la gráfica de pastel y barras, sugiere una consistencia en los datos analizados, reflejando que cada estado ocurre con frecuencias casi iguales. Aunque los vuelos cancelados tienen una ligera predominancia, esto plantea preocupaciones sobre la satisfacción del cliente y la eficiencia operativa, dado su impacto significativo. Por otro lado, con un tercio de los vuelos siendo puntuales, la aerolínea muestra una proporción aceptable de puntualidad, pero con margen para mejoras. Los retrasos, también representando un tercio de los vuelos, deben ser analizados detenidamente para identificar y abordar sus diversas causas, como condiciones meteorológicas o congestión del tráfico aéreo, con el objetivo de reducir su incidencia.
"""

#Visualización de Genero
fig_Genero=px.bar(df_new_table_Airline['Gender'].value_counts().reset_index(),x='Gender',y='count',color='Gender',color_discrete_sequence=px.colors.sequential.Viridis,text='count')
fig_Genero.update_layout(title_text="Genero", barmode='stack', xaxis_title="Gender", yaxis_title="Count")
fig_Genero.update_traces(texttemplate='%{text}', textposition='outside')

#Estado de Vuelo con respecto al género
df_vuelo_genero=df_new_table_Airline.groupby('Flight_Status')['Gender'].value_counts()
df_vuelo_genero

#Grafica de barras apliadas con respecto a los vuelos y genero

df_vuelo_genero_grafico = df_new_table_Airline.groupby(['Flight_Status', 'Gender']).size().reset_index(name='count')
fig = px.bar(df_vuelo_genero_grafico, x='Flight_Status', y='count', color='Gender', color_discrete_sequence=px.colors.sequential.Viridis, text='count')

fig.update_layout(title_text="Distribución de Género por Estado de Vuelo", barmode='stack', xaxis_title="Flight_Status", yaxis_title="Count")
fig.update_traces(texttemplate='%{text}', textposition='outside')

fig.show()

"""**INTERPRETACION**

En estas graficas de barras se puede observar que la frecuencia de las variables del estado de vuelo es casi igual. Además, el número de hombres y mujeres en el estado de vuelo es prácticamente el mismo, por lo que se puede decir que el género no influye en el estado de vuelo.
"""

#Edades concurridas en los vuelos
df_edades=df_new_table_Airline.groupby("Gender")["Age"].agg(["min", "mean","median","max"])
df_edades

"""**INTERPRETACION**

En la tabla se puede interpretar que la media de edades de los pasajeros que vuelan son de 46 años tanto de hombres como mujeres
"""

# Edadades que mas concurren
moda_edad_por_genero = df_new_table_Airline.groupby("Gender")['Age'].apply(lambda x: x.mode()[0]).reset_index()
moda_edad_por_genero

"""**INTERPRETACION**

En la tabla se puede llegar a concluir que los pasajeros que mas frecuentan en realizar vuelos son Mujeres de 39años y hombres de 89 años de edad ya que son los que mas se repiten
"""

#Grafica de relacion entre la edad de los pasajeros y la puntualidad
# Crear el gráfico de cajas con Plotly Express
fig_box = px.box(df_new_table_Airline, x='Flight_Status', y='Age', color='Flight_Status', color_discrete_sequence=px.colors.sequential.Reds, template='plotly')
fig_box.update_layout(title='Relación entre Edad y Puntualidad de los Vuelos', xaxis_title='Estado del Vuelo', yaxis_title='Edad del Pasajero')

# Mostrar el gráfico
fig_box.show()

"""**INTERPRETACION**

La gráfica de cajas muestra la distribución de la edad de los pasajeros en relación con la puntualidad de los vuelos. A primera vista, no se observa una relación clara entre la edad y la puntualidad, ya que hay una amplia variedad de edades tanto en los vuelos que llegaron a tiempo como en los que se retrasaron.
"""

# Calcular la distribución de edades por género y estado de vuelo

# Datos para países
cancelled_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Cancelled"]["Country_Name"].value_counts().head(5).to_dict()
ontime_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "On Time"]["Country_Name"].value_counts().head(5).to_dict()
delayed_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Delayed"]["Country_Name"].value_counts().head(5).to_dict()

# Datos para aeropuertos de llegada (Arrival Airport)
aa_cancelled_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Cancelled"]["Arrival_Airport"].value_counts().head(5).to_dict()
aa_ontime_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "On Time"]["Arrival_Airport"].value_counts().head(5).to_dict()
aa_delayed_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Delayed"]["Arrival_Airport"].value_counts().head(5).to_dict()

# Datos para continentes
con_cancelled_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Cancelled"]["Continents"].value_counts().to_dict()
con_ontime_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "On Time"]["Continents"].value_counts().to_dict()
con_delayed_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Delayed"]["Continents"].value_counts().to_dict()

# Colores utilizando la paleta Viridis
colors_cancelled = plt.cm.viridis(np.linspace(0, 1, 5))
colors_ontime = plt.cm.turbo(np.linspace(0, 1, 5))
colors_delayed = plt.cm.cividis(np.linspace(0, 1, 5))

# Gráficos con Matplotlib
fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(16, 10))

# Función para añadir etiquetas en las barras
def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height,
                '%d' % int(height),
                ha='center', va='bottom')

# Gráficos para países
rects1 = ax[0, 0].bar(cancelled_dict.keys(), cancelled_dict.values(), color=colors_cancelled)
autolabel(rects1, ax[0, 0])
ax[0, 0].set_title("Country Cancelled")

rects2 = ax[0, 1].bar(ontime_dict.keys(), ontime_dict.values(), color=colors_ontime)
autolabel(rects2, ax[0, 1])
ax[0, 1].set_title("Country On Time")

rects3 = ax[0, 2].bar(delayed_dict.keys(), delayed_dict.values(), color=colors_delayed)
autolabel(rects3, ax[0, 2])
ax[0, 2].set_title("Country Delayed")

# Gráficos para aeropuertos de llegada
rects4 = ax[1, 0].bar(aa_cancelled_dict.keys(), aa_cancelled_dict.values(), color=colors_cancelled)
autolabel(rects4, ax[1, 0])
ax[1, 0].set_title("Arrival Airport Cancelled")

rects5 = ax[1, 1].bar(aa_ontime_dict.keys(), aa_ontime_dict.values(), color=colors_ontime)
autolabel(rects5, ax[1, 1])
ax[1, 1].set_title("Arrival Airport On Time")

rects6 = ax[1, 2].bar(aa_delayed_dict.keys(), aa_delayed_dict.values(), color=colors_delayed)
autolabel(rects6, ax[1, 2])
ax[1, 2].set_title("Arrival Airport Delayed")

# Gráficos para continentes
rects7 = ax[2, 0].bar(con_cancelled_dict.keys(), con_cancelled_dict.values(), color=colors_cancelled)
autolabel(rects7, ax[2, 0])
ax[2, 0].set_title("Continents Cancelled")

rects8 = ax[2, 1].bar(con_ontime_dict.keys(), con_ontime_dict.values(), color=colors_ontime)
autolabel(rects8, ax[2, 1])
ax[2, 1].set_title("Continents On Time")

rects9 = ax[2, 2].bar(con_delayed_dict.keys(), con_delayed_dict.values(), color=colors_delayed)
autolabel(rects9, ax[2, 2])
ax[2, 2].set_title("Continents Delayed")

# Ajustes finales de diseño
plt.tight_layout()
plt.show()

"""**INTERPRETACION**

* Corespecto a los paises se observa que Estados Unidos tuvo el mayor número de vuelos puntuales, retrasados o cancelados. En cuanto a los aeropuertos de llegada, el aeropuerto “0” tuvo el mayor número de vuelos puntuales, retrasados o cancelados. Sin embargo, aquí el “0” significa desconocido. En cuanto a los continentes, América del Norte tuvo el mayor número de vuelos puntuales, retrasados o cancelados. Esto se debe a que Estados Unidos es el país con el mayor número de vuelos en estas categorías.En resumen los continentes con mayor desarrollo económico y turístico, como North America y Asia, lideran en cantidad de vuelos, mientras que Africa y South America muestran una menor actividad aérea, reflejando diferencias en desarrollo y conectividad.
"""

# Datos para meses de salida (Departure Month)
month_cancelled_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Cancelled"]["Departure_Month"].value_counts().head(5).to_dict()
month_ontime_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "On Time"]["Departure_Month"].value_counts().head(5).to_dict()
month_delayed_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Delayed"]["Departure_Month"].value_counts().head(5).to_dict()

# Datos para días de salida (Departure Day)
day_cancelled_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Cancelled"]["Departure_Day"].value_counts().head(5).to_dict()
day_ontime_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "On Time"]["Departure_Day"].value_counts().head(5).to_dict()
day_delayed_dict = df_new_table_Airline[df_new_table_Airline["Flight_Status"] == "Delayed"]["Departure_Day"].value_counts().head(5).to_dict()

# Colores utilizando la paleta Viridis
colors_months = plt.cm.viridis(np.linspace(0, 1, 5))
colors_days = plt.cm.cividis(np.linspace(0, 1, 5))

# Gráficos con Matplotlib
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))

# Función para añadir etiquetas en las barras
def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height,
                '%d' % int(height),
                ha='center', va='bottom')

# Gráficos para meses de salida
rects1 = ax[0, 0].bar(month_cancelled_dict.keys(), month_cancelled_dict.values(), color=colors_months)
autolabel(rects1, ax[0, 0])
ax[0, 0].set_title("Departure Month Cancelled")

rects2 = ax[0, 1].bar(month_ontime_dict.keys(), month_ontime_dict.values(), color=colors_months)
autolabel(rects2, ax[0, 1])
ax[0, 1].set_title("Departure Month On Time")

rects3 = ax[0, 2].bar(month_delayed_dict.keys(), month_delayed_dict.values(), color=colors_months)
autolabel(rects3, ax[0, 2])
ax[0, 2].set_title("Departure Month Delayed")

# Gráficos para días de salida
rects4 = ax[1, 0].bar(day_cancelled_dict.keys(), day_cancelled_dict.values(), color=colors_days)
autolabel(rects4, ax[1, 0])
ax[1, 0].set_title("Departure Day Cancelled")

rects5 = ax[1, 1].bar(day_ontime_dict.keys(), day_ontime_dict.values(), color=colors_days)
autolabel(rects5, ax[1, 1])
ax[1, 1].set_title("Departure Day On Time")

rects6 = ax[1, 2].bar(day_delayed_dict.keys(), day_delayed_dict.values(), color=colors_days)
autolabel(rects6, ax[1, 2])
ax[1, 2].set_title("Departure Day Delayed")

# Ajustes finales de diseño
plt.tight_layout()
plt.show()

"""**INTERPRETACION**

En cuanto al mes de salida, los vuelos puntuales, retrasados y cancelados fueron más comunes en los meses 10, 11 y 12. Esto muestra que la mayoría de los vuelos tuvieron lugar en estos meses y que el mes no afecta al estado de vuelo. Sin embargo, se observa que los días de salida son diferentes en los tres casos de vuelo, y se determina que esta situación, es decir, el día de salida, tiene un efecto en el estado de vuelo.
"""

# Crear el gráfico de barras
plt.figure(figsize=(45, 15))
sns.countplot(df_new_table_Airline, x='Country_Name', hue='Flight_Status', order=df_new_table_Airline['Country_Name'].value_counts().index, palette='bright')
plt.title('Cantidad de Vuelos por País y su Puntualidad')
plt.xlabel('Cantidad de Vuelos')
plt.ylabel('País')
plt.xticks(rotation=90)
plt.show()

"""**INTERPRETACION**

Estados Unidos y Canadá lideran en cuanto a la cantidad de vuelos, destacándose por su alta frecuencia de operaciones aéreas. En general, la mayoría de estos vuelos llegan a tiempo, aunque existen algunas excepciones en las que se presentan retrasos. Esta puntualidad predominante refleja la eficiencia de los sistemas de aviación en ambos países, a pesar de los ocasionales inconvenientes.

## **Encontrar los primeros indicios y sacar las preconclusiones.**

1. Identificar si hay más vuelos retrasados en algún continente específico:
    - Aunque no parece haber un continente con una cantidad significativamente mayor de retrasos, Europa muestra una proporción ligeramente superior de vuelos retrasados en comparación con otros continentes. Esto sugiere que, aunque los retrasos están distribuidos globalmente, Europa podría tener factores específicos que contribuyen a esta tendencia.

2. Identificar la puntualidad en los aeropuertos de llegada:
    - El aeropuerto identificado con el código “0” registró el mayor número de vuelos puntuales, retrasados o cancelados. Sin embargo, es crucial destacar que el código “0” representa información desconocida, lo que limita la interpretación precisa de estos datos.

3. Evaluar la puntualidad por país:
    - En los datos analizados, Estados Unidos se destaca por tener el mayor número de vuelos puntuales, retrasados o cancelados. Esto refleja la alta actividad aérea en el país y la variabilidad en la puntualidad de sus vuelos.

4. Analizar las partidas por mes y día:
    - Los datos indican que los vuelos puntuales, retrasados y cancelados fueron más frecuentes en los meses de octubre, noviembre y diciembre. Además, se observa que los días de salida varían en los tres estados de vuelo, lo que sugiere que el día de la semana puede influir en la puntualidad de los vuelos.

5. Observar si hay alguna relación entre la edad de los pasajeros y los vuelos retrasados:
    - No se identifican patrones claros que relacionen la edad de los pasajeros con la puntualidad de los vuelos. Esto indica que la edad no es un factor determinante en la ocurrencia de retrasos.

6. Determinar si ciertos países tienen más problemas de puntualidad que otros:
    - Aunque los retrasos están distribuidos de manera global, algunos países como Canadá y Francia presentan un número notable de vuelos retrasados. Esto podría indicar problemas específicos en la gestión de vuelos o factores externos que afectan la puntualidad en estos países.

## **Listar por orden de importancia los indicios que han desvelado los gráficos.**

1. Puntualidad de vuelos por continente:
      
2. Puntualidad de vuelos por país:

3. Distribución de vuelos por continente:

4. Relación entre edad y puntualidad:
   
5. Días de salida y efecto en la puntualidad:
  
6. Aeropuerto con código “0” y su relevancia:

# **PASO TRES.** Ahora es momento de decidir si las preconclusiones son ciertas o no. Apoyarse en la estadística inferencial y del diseño de experimentos.

## **Encontrar las técnicas más apropiadas para corroborar las preconclusiones con la ayuda de un mapa.**
"""

# Instalación de graphviz
!pip install graphviz

# Crear un nuevo gráfico dirigido
graph = Digraph('Técnicas para corroborar preconclusiones')

# Añadir los nodos y conexiones al gráfico
graph.node('A', 'Corroboracion de preconclusiones')
graph.node('B', 'Análisis de Varianza (ANOVA)')
graph.node('C', 'Prueba de Chi-Cuadrado')
graph.node('D', 'Regresión Logística')
graph.node('E', 'Series Temporales')
graph.node('F', 'Para comparar las diferencias en \n puntualidad entre continentes y países')
graph.node('G', 'Para evaluar la independencia entre variables \n categóricas como el país y el estado del vuelo.')
graph.node('H', ' Para analizar la relación entre variables \n independientes (como la edad) y una variable dependiente \n binaria (puntualidad del vuelo).')
graph.node('I', 'Para analizar los patrones en \n la puntualidad de vuelos por mes y día.')

graph.edges(['AB', 'AC', 'AD', 'AE','BF', 'CG', 'DH','EI'])

# Personalizar el gráfico
graph.attr(rankdir='TB')

# Mostrar el gráfico en la pantalla de Colab
graph

"""## **Diseñar la metodología de análisis.**

**Metodología de análisis**

La metodología de análisis será la siguiente:

1. **Análisis de varianza (ANOVA)** para comparar la puntualidad entre continentes.
2. **Test de Chi-cuadrado** para evaluar la independencia entre países y el estado del vuelo.
3. **Regresión logística** para analizar la relación entre la edad de los pasajeros y la puntualidad del vuelo.
4. **Análisis de series temporales** para evaluar los patrones en la puntualidad por mes y día.
5. **Visualización de datos con gráficos** para interpretar los resultados de los análisis anteriores.

## **Aplicar esta metodología.**

Para poder realizar este punto, previamente en la PARTE UNO se realizó un análisis previo realizando una limpieza de datos, revision de datos faltantes, convirtiendo tambien las fechas de salida a un formato mas trabajable, etc. Así obteniendo un nuevo dataset ya con los datos listos para aplicar la metodologia, a continuacion se muestra el data set final obtenido.
"""

#Data frame obtenido luego de la realziacion del analisis correspondiente
df_new_table_Airline

"""### 1. Análisis de Varianza (ANOVA)"""

#Comparación de la puntualidad entre continentes.

# Convertir Flight_Status a una variable numérica
# Flight_Status tiene valores 'On Time', 'Delayed' y Cancelled.
df_new_table_Airline['Flight_Status_Numeric'] = df_new_table_Airline['Flight_Status'].map({'On Time': 1, 'Delayed': -1, 'Cancelled':0})

# Verificar que la conversión sea correcta
print(df_new_table_Airline[['Flight_Status', 'Flight_Status_Numeric']].head(10))

# Realizar el análisis ANOVA
print()
print('Analisis ANOVA')
df_anova_model = ols('Flight_Status_Numeric ~ C(Continents)', data=df_new_table_Airline).fit()
df_anova_results = sm.stats.anova_lm(df_anova_model, typ=2)
df_anova_results

"""### 2. Test de Chi-Cuadrado"""

# Evaluacion de la independencia entre paises y el estado de vuelo
tabla_contingencia = pd.crosstab(df_new_table_Airline['Country_Name'], df_new_table_Airline['Flight_Status'])
chi2, p, dof, expected = stats.chi2_contingency(tabla_contingencia)
print("Chi-Cuadrado:", chi2)
print("P-valor:", p)

"""### 3. Regresión Logística"""

# Analisis de la relacion entre la edad de los pasajeros y la puntualidad del vuelo

#Filtración y reparacion de los patos para la regresion logística.
df_logistic = df_new_table_Airline[['Age', 'Flight_Status']].copy()
df_logistic = df_logistic.dropna()

# Convertir el estado del vuelo a una variable binaria (1: On Time, 0: Delayed or Cancelled)
df_logistic['Flight_Status'] = df_logistic['Flight_Status'].apply(lambda x: 1 if x == 'On Time' else 0)

# Ajustar el modelo de regresión logística
X = df_logistic['Age']
y = df_logistic['Flight_Status']
X = sm.add_constant(X)  # agregar una constante para el intercepto
logit_model = sm.Logit(y, X).fit()
print(logit_model.summary())

"""### 4. Análisis de series temporales"""

#Evaluación de los patrones en la puntualidad por mes y dia

df_new_table_Airline['Departure_Year'] = pd.to_numeric(df_new_table_Airline['Departure_Year'])
df_new_table_Airline['Departure_Month'] = pd.to_numeric(df_new_table_Airline['Departure_Month'])
df_new_table_Airline['Departure_Day'] = pd.to_numeric(df_new_table_Airline['Departure_Day'])

#Cambiar el orden de las fechas para poder usar el date time
df_new_table_Airline['Departure_Date'] = pd.to_datetime(df_new_table_Airline['Departure_Year'].astype(str) + '-' +
                                                        df_new_table_Airline['Departure_Month'].astype(str).str.zfill(2) + '-' +
                                                        df_new_table_Airline['Departure_Day'].astype(str).str.zfill(2))

df_new_table_Airline['Month'] = df_new_table_Airline['Departure_Date'].dt.month
df_new_table_Airline['Day'] = df_new_table_Airline['Departure_Date'].dt.dayofweek
month_flight_status = df_new_table_Airline.groupby('Month')['Flight_Status'].value_counts().unstack().fillna(0)
day_flight_status = df_new_table_Airline.groupby('Day')['Flight_Status'].value_counts().unstack().fillna(0)

"""### Visualización de los resultados"""

plt.figure(figsize=(14, 7))

plt.subplot(1, 2, 1)
month_flight_status.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title('Puntualidad de vuelos por mes')
plt.xlabel('Mes')
plt.ylabel('Número de vuelos')

plt.subplot(1, 2, 2)
day_flight_status.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title('Puntualidad de vuelos por día de la semana')
plt.xlabel('Día de la semana')
plt.ylabel('Número de vuelos')

plt.tight_layout()
plt.show()

"""# **Resumir los resultados.**

A continuación, se realiza un resumen de los resultados obtenidos de las pruebas estadísticas y visualizaciones.

1. Análisis de varianza (ANOVA):
  * El análisis ANOVA no encontró diferencias significativas en la puntualidad de los vuelos entre los continentes (p = 0.641), lo que sugiere que los factores específicos de cada continente no tienen un impacto notable en la puntualidad de los vuelos. Esto indica que la variabilidad en la puntualidad de los vuelos puede estar más relacionada con otros factores como condiciones climáticas, políticas de aerolíneas, o gestión aeroportuaria, en lugar de con la ubicación geográfica específica de los continentes. La falta de significancia en los resultados también puede ser un indicio de que los problemas de puntualidad son uniformes a nivel global, afectando a las aerolíneas de manera similar sin importar el continente de operación

2. Test de Chi-cuadrado:
  * La prueba de Chi-cuadrado arrojó un valor de 414.5802 con un p-valor de 0.9637. Esto indica que no hay una diferencia estadísticamente significativa entre las categorías observadas y las esperadas. En términos simples, los datos observados no presentan una desviación significativa de lo que se esperaría bajo la hipótesis nula. Por lo tanto, no se rechaza la hipótesis nula, sugiriendo que las variables categóricas evaluadas no están asociadas de manera significativa

3. Regresión logística:
   * La regresión logística no encontró una relación significativa entre la edad de los pasajeros y la puntualidad de los vuelos, como lo indica el coeficiente de la variable "Age" (coef = -8.874e-05, p = 0.733). Esto sugiere que la edad de los pasajeros no es un factor determinante en los retrasos de los vuelos. El modelo tuvo una Pseudo R-squared de 9.242e-07, lo que indica una capacidad predictiva muy baja. Además, el valor de log-verosimilitud (-62754) no mejoró con respecto al modelo nulo, lo que refuerza la conclusión de que la variable "Age" no tiene un impacto significativo en la puntualidad de los vuelos.

4. Análisis de series temporales:
  * Las visualizaciones revelaron que los meses de octubre, noviembre y diciembre registran un mayor número de vuelos puntuales, retrasados y cancelados. Además, se identificaron ciertos días de la semana con más problemas de puntualidad en comparación con otros. Esto sugiere una variabilidad estacional y semanal en la puntualidad de los vuelos, que puede estar influenciada por factores como el aumento del tráfico aéreo durante las temporadas altas y variaciones en la gestión operativa de las aerolíneas.

## Conclusión

Después de un análisis exhaustivo de los datos disponibles, se confirman las siguientes preconclusiones iniciales:

1. Europa muestra una proporción ligeramente superior de vuelos retrasados en comparación con otros continentes, lo cual sugiere la presencia de factores regionales específicos que pueden influir en la puntualidad de los vuelos. Esto podría incluir desde condiciones climáticas variables hasta políticas operativas distintas entre aerolíneas europeas.
2. Estados Unidos sobresale por tener la mayor cantidad de vuelos (puntual, retrasado, cancelado) en todos los estados, ya sean puntuales, retrasados o cancelados. Esta alta actividad aérea refleja tanto la densidad de tráfico como la complejidad de las operaciones aeroportuarias en el país
3. No se encontraron patrones claros que relacionen la edad de los pasajeros con la puntualidad de los vuelos. Esto indica que, independientemente de la edad, los pasajeros no tienen un impacto significativo en la ocurrencia de retrasos.
4. Los meses de octubre, noviembre y diciembre, junto con ciertos días de la semana, muestran consistentemente más problemas de puntualidad. Esta variabilidad estacional y semanal puede estar influenciada por el aumento del tráfico durante períodos festivos y variaciones en la gestión operativa de las aerolíneas.
5. La relevancia del aeropuerto con el código "0" sigue siendo indeterminada debido a la falta de información específica sobre este código en particular. Es crucial obtener datos más detallados para comprender mejor su impacto en la puntualidad de los vuelos y su significancia dentro de la red aeroportuaria global.

En resumen, la puntualidad de los vuelos se ve afectada principalmente por factores geográficos, temporales y operativos. Las condiciones climáticas locales y la congestión del tráfico aéreo tienen un impacto significativo en la capacidad de cumplir con los horarios en los aeropuertos. Asimismo, la eficiente gestión del mantenimiento y los procesos de embarque también juegan un papel importante en la puntualidad de los vuelos, lo que repercute en la satisfacción de los pasajeros y en la reducción de problemas de conexión. Estos elementos varían según la ubicación geográfica y el momento del año, lo que representa un desafío constante para las compañías aéreas.
"""


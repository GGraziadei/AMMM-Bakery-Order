import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Dati forniti
data = [
    {
                    "eliteProp": 0.2,
                    "mutantProp": 0.1,
                    "inheritanceProb": 0.7,
                    "ObjValue": 0.776,
    },
    {"eliteProp": 0.1, "mutantProp": 0.1, "inheritanceProb": 0.1, "ObjValue": 0.78661331},
    {"eliteProp": 0.1, "mutantProp": 0.1, "inheritanceProb": 0.3, "ObjValue": 0.78066440},
    {"eliteProp": 0.1, "mutantProp": 0.1, "inheritanceProb": 0.5, "ObjValue": 0.78241500},
    {"eliteProp": 0.1, "mutantProp": 0.1, "inheritanceProb": 0.5, "ObjValue": 0.78102756},

    {"eliteProp": 0.2, "mutantProp": 0.1, "inheritanceProb": 0.1, "ObjValue": 0.78212353},
    {"eliteProp": 0.2, "mutantProp": 0.1, "inheritanceProb": 0.3, "ObjValue": 0.78423456},
    {"eliteProp": 0.2, "mutantProp": 0.1, "inheritanceProb": 0.5, "ObjValue": 0.78567834},
    {"eliteProp": 0.3, "mutantProp": 0.1, "inheritanceProb": 0.1, "ObjValue": 0.78345678},
    {"eliteProp": 0.3, "mutantProp": 0.1, "inheritanceProb": 0.3, "ObjValue": 0.78123456},
    {"eliteProp": 0.3, "mutantProp": 0.1, "inheritanceProb": 0.5, "ObjValue": 0.78456789},
    # Aggiungi altri dati
]

# Estrai i valori di Obj.value e gli altri parametri
elite_props = [entry["eliteProp"] for entry in data]
mutant_props = [entry["mutantProp"] for entry in data]
inheritance_probs = [entry["inheritanceProb"] for entry in data]
obj_values = [entry["ObjValue"] for entry in data]

# Crea un grafico 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grafico 3D
scatter = ax.scatter(elite_props, mutant_props, inheritance_probs, c=obj_values, cmap='viridis')

# Etichette degli assi
ax.set_xlabel('Elite Prop')
ax.set_ylabel('Mutant Prop')
ax.set_zlabel('Inheritance Prob')
ax.set_title('Obj.value')

# Barra dei colori
cbar = fig.colorbar(scatter)
cbar.set_label('Obj.value')

# Mostra il grafico
plt.show()

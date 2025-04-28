import src.idkSIM as idkSIM
import os, sys, time
start_time = time.time()

sys.path.insert(0, os.path.abspath(r"D:/idk_framework/idkROM")) # para no tener que instalar idkROM como paquete
sys.path.insert(0, os.path.abspath(r"D:/idk_framework/idkFEM")) # para no tener que instalar idkFEM como paquete

#idkSIM.runIdkSIM("optim_idkROM.yml") # idkROM está instalado como paquete?
#idkSIM.runIdkSIM("hyperparameter_optim.yml")
#idkSIM.runIdkSIM("optim_idkFEM.yml")
#idkSIM.runIdkSIM("minimize_idkfem.yml")
idkSIM.runIdkSIM("doe_idkfem.yml") # idkROM está instalado como paquete?

total_time = time.time() - start_time
print('Aplicación ejecutada correctamente')
print("--- %s seconds ---" % (time.time() - start_time)) 
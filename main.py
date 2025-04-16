import src.idkSIM as idkSIM
import time
start_time = time.time()


idkSIM.runIdkSIM("main_optimROM.yml")
#idkSIM.runIdkSIM("hyperparameter_optim.yml")

total_time = time.time() - start_time
print('Aplicación ejecutada correctamente')
print("--- %s seconds ---" % (time.time() - start_time))
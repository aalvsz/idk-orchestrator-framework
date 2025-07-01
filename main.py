import src.idkSIM as idkSIM

import os, sys, time
start_time = time.time()

# hacer commit de idkFEM
sys.path.insert(0, os.path.abspath(r"D:/idk_framework/idkFEM")) # para no tener que instalar idkFEM como paquete


if __name__ == "__main__": # para parelizacion, es necesaria la estructura if __name__ == "__main__":

    idkSIM.runIdkSIM("yml/optim_idkROM.yml") 
    #idkSIM.runIdkSIM("yml/hyperparameter_optim.yml")
    #idkSIM.runIdkSIM("yml/optim_idkFEM.yml")
    #idkSIM.runIdkSIM("yml/minimize_idkfem.yml")
    #idkSIM.runIdkSIM("yml/doe_travesano_idkfem.yml") 
    #idkSIM.runIdkSIM("yml/train_rom_NN.yml")
    
    #idkSIM.runIdkSIM("yml/optim_simulink.yml")

    #idkSIM.runIdkSIM("yml/optim_test.yml")

    total_time = time.time() - start_time
    print('Aplicación ejecutada correctamente')
    print("--- %s seconds ---" % (time.time() - start_time))

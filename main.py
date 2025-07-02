import src.idkSIM as idkSIM

import os, sys, time
start_time = time.time()

def __test_idkFEM():
    from src.tests.idkfem_engine import quick_run
    quick_run()


def __test_idkROM():
    from src.tests.idkrom_engine import quick_run
    quick_run()

if __name__ == "__main__": # para parelizacion, es necesaria la estructura if __name__ == "__main__":

    #idkSIM.runIdkSIM("yml/optim_idkROM.yml") 
    #idkSIM.runIdkSIM("yml/hyperparameter_optim.yml")
    #idkSIM.runIdkSIM("yml/optim_idkFEM.yml")
    #idkSIM.runIdkSIM("yml/minimize_idkfem.yml")
    #idkSIM.runIdkSIM("yml/doe_travesano_idkfem.yml") 
    #idkSIM.runIdkSIM("yml/train_rom_NN.yml")
    
    #idkSIM.runIdkSIM("yml/optim_simulink.yml")

    #idkSIM.runIdkSIM("yml/optim_test.yml")

    #__test_idkFEM()
    __test_idkROM()

    total_time = time.time() - start_time
    print('Aplicación ejecutada correctamente')
    print("--- %s seconds ---" % (time.time() - start_time))

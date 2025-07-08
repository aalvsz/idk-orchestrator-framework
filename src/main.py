import idksim.idkSIM as idkSIM

import os, sys, time
start_time = time.time()

def __test_idkFEM():
    from idksim.borrador.idkfem_engine import quick_run
    quick_run()


def __test_idkROM():
    from idksim.borrador.idkrom_engine import quick_run
    quick_run()

if __name__ == "__main__": # para parelizacion, es necesaria la estructura if __name__ == "__main__":
    
    idkSIM.runIdkSIM(r"D:\idk_framework\idksimulation\yml\test_functions\minimize_curvefit.yml")

    #__test_idkFEM()
    #__test_idkROM()

    total_time = time.time() - start_time
    print('Aplicación ejecutada correctamente')
    print("--- %s seconds ---" % (time.time() - start_time))

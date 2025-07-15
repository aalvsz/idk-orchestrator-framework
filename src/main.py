import idksim.idkSIM as idkSIM

import os, sys, time
start_time = time.time()


if __name__ == "__main__":
    
    idkSIM.runIdkSIM(r"D:\idk_framework\idksimulation\yml\test_functions\parabola_nsga2.yml")

    total_time = time.time() - start_time
    print('Aplicación ejecutada correctamente')
    print("--- %s seconds ---" % (time.time() - start_time))

from idkfem.idkFEM import idkFEM_loader


parametros_modelo = {
    # Malla
    'mesh_size'      : 0.03,             # Tamaño de malla (m)

    # Rigidez patines Travesaño - Pedestal (RUE 45-E-L)
    'K_YX'           : 694.5e6,          # Rigidez en Y (N/m)
    'K_ZX'           : 687.5e6,          # Rigidez en Z (N/m)

    # Rigidez patines Travesaño - Consola (RUE 55-E-L)
    'K_XY'           : 833.5e6,          # Rigidez en X (N/m)
    'K_ZY'           : 823.8e6,          # Rigidez en Z (N/m)

    # Espesores de paredes externas (Geometría)
    't_front'        : 30.0e-3,          # Espesor cara frontal (m) --> Límites: [20.0e-3 - 45.0e-3]
    't_rear'         : 30.0e-3,          # Espesor cara trasera (m) --> Límites: [20.0e-3 - 45.0e-3]
    't_top'          : 30.0e-3,          # Espesor cara superior (m) --> Límites: [20.0e-3 - 45.0e-3]
    't_bottom'       : 30.0e-3,          # Espesor cara inferior (m) --> Límites: [20.0e-3 - 45.0e-3]
    't_lateral'      : 30.0e-3,          # Espesor cara lateral 1 (m) --> Límites: [20.0e-3 - 45.0e-3]

    # Nervios longitudinales
    't1_long'        : 20.0e-3,          # Espesor central del nervio longitudinal (m) --> Límites: [30.0e-3 - 60.0e-3]
    't2_long'        : 20.0e-3,          # Espesor lateral del nervio longitudinal (m) --> Límites: [15.0e-3 - 45.0e-3]
    'h_long'         : 130.0e-3,         # Altura del nervio longitudinal (m) --> Límites: [100.0e-3 - 200.0e-3]

    # Nervios transversales
    't1_trans'       : 30.0e-3,          # Espesor del nervio transversal central (m) [20.0e-3 - 40.0e-3]
    't2_trans'       : 30.0e-3,          # Espesor del nervio transversal lateral (m) [20.0e-3 - 40.0e-3]
    'd_t_trans'      : 0.5,              # Posicion del punto intermedio en modo relativo (-) --> Límites: [0.1 - 0.9]
    'inc_t_trans'    : 0,              # Incremento en el espesor del punto intermedio respecto al valor medio del espesor en los dos extremos (-) --> Límites: [-0.5 - 0.5]
    'K_trans'        : 1.0,              # Constante de distancia entre nervios d_i = K*d_(i-1) (-)
    'N_trans'        : 2,                # Nº de nervios por parte simétrica
    'ang_Z'          : 0,                # Ángulo de orientación sobre Z (°)

    # Diámetro vaciado nervios
    'D'              : 650.0e-3          # Diámetro del agujero (m)
}

object_dict = {'pFEM1': r"D:\test\Travesano.yml", 'pFEM2': r"D:\test\Carro.yml"}

def quick_run(input_dict = parametros_modelo, objects = object_dict):

    obj = idkFEM_loader(main_yml = r"D:\test\main.yml", objects = objects) # Genera objeto de idkFEM con path del main.yml
    if input_dict is not None:
        res_idkFEM = obj.idk_run(dict=input_dict)
    else:
        res_idkFEM = obj.idk_run()

    return res_idkFEM
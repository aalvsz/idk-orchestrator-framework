from idkrom.model import idkROM

NN_dict_hyperparams = {'n_capas': 5, 'n_neuronas': 32, 'activation': 'ReLU',
                        'dropout_rate': 0.1, 'optimizer_nn': 'Adam', 'lr': 0.01,
                         'lr_decrease_rate': 0.5, 'epochs': 5000,
                          'batch_size': 64, 'patience': 100, 'cv_folds': 5,
                            'convergence_threshold': 1e-5}

def quick_run():
    rom_instance = idkROM(random_state=41, config_yml_path=r"D:\test\config.yml")
    rom_instance.idk_run(dict_hyperparams=None)
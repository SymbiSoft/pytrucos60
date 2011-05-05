#-*- coding: utf-8 -*-
#!/usr/bin/env python
"""Ponto de execução para o jogo.

Configura o módulo caminho e bibliotecas e em seguida, chama lib.main.main.

"""

import os
import sys
import traceback


def prepara_path():
    """Carrega o diretório fonte no sys.path.

    Isso só será necessário quando estiver executando uma distribuição fonte. 
    Distribuições binária já garantem que o caminho do módulo contém os módulos 
    de qualquer maneira.

    """
    if os.path.exists("gamelib"):
        sys.path.insert(1, "gamelib")




def set_debug(debug):
    """Defina o sinalizador de debug no módulo constantes para o valor determinado.
    

    :Parametros:
        `debug` : bool
            O valor definido.

    """
    try:
        import constantes
        constantes.DEBUG = debug
    except ImportError, exc:
        print "error: não foi possível encontrar diretório de origem eueueu"
        sys.exit(1)



def setup_logging():
    import logging
    import constantes
 
    if constantes.DEBUG:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.CRITICAL
        
    #loglevel = logging.INFO    
    logging.basicConfig(level = loglevel,
                        format   ='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt  ='%H:%M:%S', filename = constantes.LOGFILE, filemode = 'w')
                        
    console = logging.StreamHandler()
    console.setLevel(loglevel)

    formatter = logging.Formatter('%(name)-12s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
     
def run(debug=False):
    """Executa o jogo.

    Prepares the top level before launching the game. The aim is to make moving
    from development to production simple, and to ensure differences between
    distributions are ironed out before starting the game.

    :Parameters:
        `debug` : bool
            The value to set for constantes.DEBUG.

    """
    prepara_path()
    set_debug(debug)
    setup_logging()
    
    try:
        import main
        main.run()
    except Exception, exc:
        import constantes
        open(constantes.TMP_LOC+constantes.CONFIG_NAME+"_error.log", "w").write(traceback.format_exc())
        raise


if __name__ == "__main__":

    # Change to the game directory
    os.chdir(os.path.dirname(os.path.join(".", sys.argv[0])))

    # Start the actual game
    run()
#-*- coding: utf-8 -*-

"""Configuration parameters stored in a module namespace.

Este arquivo é carregado durante a inicialização do programa, antes de o módulo 
principal ser importado. Consequentemente, este arquivo não deve importar qualquer 
outro módulo, ou os módulos serão inicializados antes do módulo principal, o que 
significa que as opções de linha de comando pode não ter sido registradas.

Parâmetros vêm em dois tipos, aqueles que são armazenados no arquivo de 
configuração e aqueles que não são. Executar o Profiler é um exemplo do 
primeiro; modo de tela cheia seria um exemplo deste último.

Só porque uma opção é armazenada no arquivo de configuração, não significa que 
ela também não possa ser alterada. Por exemplo, uma alteração de linha de comando. 
Mas isso não deve alterar o valor do arquivo de configuração.

O método 'save_option' é usado para alterar um valor aqui e no arquivo de configuração.
Ele só pode ser chamado por uma lista predefinida de opções. O método 'save_all' 
provavelmente não deve ser usado. Ele irá escrever todos os valores atuais por 
parâmetros do arquivo de configuração para o arquivo de configuração.

"""

# IMPORTANT!
# Nunca faça "from config import ...". Este módulo baseia-se na manipulação de 
# seu próprio namespace para funcionar corretamente.
__all__ = []


class LocalConfig(object):
    """Gerencia o arquivo de configuração local.

    """

    def __init__(self, **defaults):
        """Cria um objeto LocalConfig.

           Argumentos palavra-chave defini o import das opções de configurações locais  e seus valores padrão.
        
        """
        self.defaults = defaults
        self.locals = dict(defaults)
        self.load()

    @property
    def config_path(self):
        """O caminho para o arquivo de configuração de usuario local.

        """
        import constantes, os, pyglet
        config_dir = pyglet.resource.get_settings_path(constantes.CONFIG_NAME)
        if not os.path.exists(config_dir): os.makedirs(config_dir)
        config_path = os.path.join(config_dir, "local.py")
        #print "config path:"+config_path
        open(config_path, "a").close()
        return config_path

    def load(self):
        """Lê o arquivo de configuação.

        """
        config_scope = {}
        exec open(self.config_path) in config_scope
        for name in self.defaults:
            value = config_scope.get(name, self.defaults[name])
            self.locals[name] = globals()[name] = value

    def save(self):
        """Escreve no arquivo de configuração.

        """
        config_fd = open(self.config_path, "w")
        for key in self.defaults:
            value = self.locals[key]
            if value != self.defaults[key]:
                line = "%s = %r\n" % (key, value)
                config_fd.write(line)
        config_fd.close()

    def save_option(self, name, value=None):
        """Alterar uma opção no arquivo de configuração.

        :Parametros:
            `name` : str
                O nome da opção para salvar.
            `value` : object
                O valor a ser definido.

        """
        assert name in self.defaults
        if value is not None:
            globals()[name] = value
        self.locals[name] = globals()[name]
        self.save()

    def save_all(self):
        """ Salva todos os valores atuais para o arquivo de configuração.

        """
        for name in self.defaults:
            self.locals[name] = globals()[name]
        self.save()


# Valores padrão para as opções não-persistentes.
profile = False

# Valores padrão para opções persistentes.
local = LocalConfig(
    fullscreen = False,
    playername = "",
    playerseed = "",
    musicvolume = 10,
    sfxvolume = 10,
    arqjogo = "jogo", # por exemplo
    )

# Veja o módulo docstring para obter detalhes sobre esses métodos.
save_option = local.save_option
save_all = local.save_all

# Limpa o modulo do namespace.
del local, LocalConfig

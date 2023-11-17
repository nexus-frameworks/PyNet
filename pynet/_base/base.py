class Base:
    def __init__(self, **kwargs) -> None: 
        self.__threads = []
        self.__conns = []
        self.__configs = kwargs

    @property
    def threads(self) -> list:
        return self.__threads
    
    @property
    def conns(self) -> list:
        return self.__conns
    
    def show_configs(self) -> dict:
        return self.__configs

    def reconfig(self, **kwargs): 
        self.__configs = kwargs
        return self
    
    def reset_configs(self) -> None:
        self.__configs.clear()
    
    configs = property(show_configs, reconfig, reset_configs)

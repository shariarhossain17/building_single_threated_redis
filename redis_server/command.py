class CommandHandler:
    def __init__(self,storage):
        self.storage=storage
        self.command={
            "PING":self.ping,
            "ECHO":self.echo,
            "SET":self.set,
            "GET":self.get,
            "DEL":self.delete,
            "EXIST":self.exist,
            "KEYS":self.keys,
            "FLUSHALL":self.flushall,
            "INFO":self.info
        }
    

    def execute(self,command,*args):
        cmd=self.command.get(command.upper())
        if cmd:
            return cmd(*args)
        else:
            return error(f"unknown command `{command}")
    
    
    def get(self,*args):
        if len(args)!=1:
            return error("wrong number of argument for get command")
        return b"\r\nfrom get"
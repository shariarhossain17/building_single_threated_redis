from .response import *


class CommandHandler:
    def __init__(self,storage):
        self.storage=storage
        self.command={
            "PING":self.ping,
            "ECHO":self.echo,
            "SET":self.set,
            "GET":self.get,
            # "DEL":self.delete,
            # "EXIST":self.exist,
            # "KEYS":self.keys,
            # "FLUSHALL":self.flushall,
            # "INFO":self.info
        }
    

    def execute(self,command,*args):
        cmd=self.command.get(command.upper())
        print(cmd,"from execute")
        if cmd:
            return cmd(*args)
        else:
            return error(f"unknown command `{command}")
    def ping(self,*args):
        return pong()
    

    def echo(self,*args):
        return simple_string(" ".join(args) if args else simple_string(""))
    

    def set(self,*args):
        if len(args)<2:
            return error("wrong number of argument for set")
        self.storage.set(args[0]," ".join(args[1:]))
        return ok()
    
    def get(self,*args):
        if(len(args)!=1):
            return error("wrong number argument for 'get' command")
        return bulk_string(self.storage.get(args[0]))
        
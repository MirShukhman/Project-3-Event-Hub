import json
import os
from datetime import datetime

# 24.02.24
# Mir Shukhman
#Defining the class Logger to create a running log of every func run from "Repository" class
class Logger(object):
    _instance = None
    _log_file = 'log.json'
    
    def __new__(cls):
        """
        24.02.24
        Mir Shukhman
        Func to define class Logger as "singelton" to avoide duplications of "log"
        And initial creation of log.json as part of cretion of the class instance
        Returns class instance
        """
        if cls._instance is None:
            cls._instance= super(Logger,cls).__new__(cls)
            # Creating the log file as part of the instance creation, if not alredy exists
            if not os.path.exists(cls._log_file):
                with open(cls._log_file, 'w') as file:
                    file.write('[]')
            
        return cls._instance
    
    def __init__(self)-> None:
        pass
        
    @property
    def log_path(self):
        """
        24.02.24
        Mir Shukhman
        Func getter returns path to the log file
        """
        return self._log_file
    
   
    def log(self, class_name, func_name, func_input, func_output):
        """
        24.02.24
        Mir Shukhman
        Func to add log entry
        Input: func name, func's input, func's output. Datetime + id set automaticly
        Ouput: None/err(str)
        """
        id = self.count_entries()+1
        log_entry = {
            'id': id,
            'datetime': str(datetime.now()),
            'class-name': str(class_name),
            'func_name': str(func_name),
            'func_input': str(func_input),
            'func_output': str(func_output)
        }
        
        try:
            with open(self._log_file, 'r') as file:
                try:
                    log_entries = json.load(file)
                except json.JSONDecodeError:
                    log_entries = []

            log_entries.append(log_entry)

            with open(self._log_file, 'w') as file:
                json.dump(log_entries, file, indent=2)
                
        except Exception as e:
            return str(e)
        

    def count_entries(self):
        """
        24.02.24
        Mir Shukhman
        Count the number of entries in the log file.
        Input: None
        Output: lenoffile (int)/0 if err
        """
        try:
            with open(self._log_file, 'r') as file:
                log_entries = json.load(file)
                return len(log_entries)
        except json.JSONDecodeError:
            return 0
        
        except FileNotFoundError:
            return 0


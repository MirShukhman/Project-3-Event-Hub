
import jwt
from app import create_app
import json
import os
import time
import threading
from app import bcrypt

# 25.02.24
# Mir Shukhman
# Defining class LoginToken witch will recive token data (preset to none),
#   generate jwt token, save the token in json file and return the path, 
#   then return token data to none, and preset a timer to delete the json 
#   file after 3 hrs. Also holds the delete file func.


class LoginToken:
    def __init__(self,_token_data=None, filename='token.json' ):
        self._token_data = _token_data
        self.module_dir = os.path.dirname(os.path.realpath(__file__))
        self.filename = filename
        self.filepath = os.path.join(self.module_dir, self.filename) 

    @property
    def login_token(self):
        """
        25.02.24
        Mir Shukhman
        Calls for jwt token generator func
        """
        return self._generate_jwt_token()
    
    @property
    def token_data(self):
        """
        25.02.24
        Mir Shukhman
        Token Data getter
        """
        return self._token_data 

    @token_data.setter
    def token_data(self, values):
        """
        25.02.24
        Mir Shukhman
        Token Data setter
        """
        self._token_data  = values
        
    def _generate_jwt_token(self):
        """
        25.02.24
        Mir Shukhman
        Generates jwt token, shoves to json file, 
        encrypts th token to be passed to front end,
        resets token_data to None, 
        creates a thread that calls sceduale deletion func.
        ***Inner func***
        Output: json file path with jwt token; or error
        """
        if all(value is not None for value in self.token_data):
            token = jwt.encode(
                {'ID': self.token_data[0],
                 'name': self.token_data[1],
                 'is_master_user': self.token_data[2]},
                create_app().config['SECRET_KEY'],
                algorithm='HS256'
            )
            
            with open(self.filepath, 'w') as json_file:
                json.dump(token, json_file)
            front_end_token = bcrypt.generate_password_hash(token).decode('utf-8')
            self.token_data = None
            threading.Thread(target=self._schedule_token_file_deletion, args=(3,), daemon=True).start()
             
            return (self.filepath, front_end_token)
        
        else:
            return False
        
    
    def _schedule_token_file_deletion(self, delay_hours):
        """
        26.02.24
        Mir Shukhman
        Starts timer for 3 hrs, after witch calls delete file func 
        ***Inner func***
        """
        delay_seconds = delay_hours * 60 * 60
        time.sleep(delay_seconds)

        self.delete_token_file()
        
        
    def delete_token_file(self):
        """
        26.02.24
        Mir Shukhman
        Deletes json file
        Input: json file
        Output: True; None if file not found
        """
        try:
            os.remove(self.filepath)
            return True
        except FileNotFoundError:
            return None

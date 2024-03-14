
import jwt
import json
from app import create_app
from app import bcrypt

class Authenticator:
    
    def __init__(self, file_path):
        self.file_path = file_path
    
    
    def _read_and_decode_jwt(self):
        try:
            with open(self.file_path, 'r') as json_file:
                token = json.load(json_file)
                secret_key = create_app().config['SECRET_KEY']
                decoded_data = jwt.decode(token, secret_key, algorithms=['HS256'])
                return decoded_data
            
        except Exception as e:
            return None
        
    
    def authenticate_user(self, front_end_token):
        try:
            with open(self.file_path, 'r') as json_file:
                token = json.load(json_file)
            if token:
                authentication=bcrypt.check_password_hash(front_end_token, token)
                if authentication:
                    return True
            else:
                return False
                    
        except Exception as e:
            return False
        
           
    def get_user_id(self):
        try:
            decoded_token= self._read_and_decode_jwt()
            if decoded_token:
                user_id = decoded_token.get('ID', None)
                return user_id
            
            else:
                return False
            
        except Exception as e:
            return False
        
     
    def get_user_fullname(self):
        try:
            decoded_token= self._read_and_decode_jwt()
            if decoded_token:
                fullname = decoded_token.get('name', None)
                return fullname
            
            else:
                return False
            
        except Exception as e:
            return False
        
           
    def get_master_approval(self):
        try:
            decoded_token= self._read_and_decode_jwt()
            if decoded_token:
                isMaster = decoded_token.get('is_master_user', None)
                return isMaster
            
            else:
                return False
            
        except Exception as e:
            return False
        
        
    

from app import bcrypt
from datetime import datetime

from modules.event_categories import EventCategories
from modules.event_images import EventImages
from modules.events import Events
from modules.feedback import Feedback
from modules.registrations import Registrations
from modules.users import Users
from modules.repository import Repository
from logger import Logger
from backend_logic.login_token import LoginToken

# 25.02.24
# Mir Shukhman
# Defining class BackendBase wich will be parent class for all other backend classes
# Every use of one of Backend's funcs will be logged in 'log.json' in format:
#       id(Auto-generated), dattime(Auto-generated), class_name, func_name, func_input, func_output

class BackendBase:
    def __init__(self):
        self.class_name=self.__class__.__name__
        # Instance of logger to acsess the log func from Logger class
        self.logger = Logger()
        # Instances of Repository class with all the db.models as parameters 
        #       to utilise Repo's funcs in the backend classes' funcs
        self.categories_repo= Repository(EventCategories)
        self.images_repo= Repository(EventImages)
        self.events_repo= Repository(Events)
        self.feedback_repo= Repository(Feedback)
        self.registrations_repo= Repository(Registrations)
        self.users_repo= Repository(Users)
        self.lt_instance=LoginToken()


    def _check_password(self,hashed_password,password):
        result= bcrypt.check_password_hash(hashed_password, password)
        self.logger.log(self.class_name,'_check_password', hashed_password, result)
        return result


    def login (self,*, username, password):
        err_msg = None
        try:
            # look for user by username(SP)
            user=self.users_repo.get_stored_procedure(
                    'get_user_by_username',{'username':username})
            if user:
                db_pass= user[0][2] 
                is_master_user= user[0][8]
                user_ID = user[0][0]
                name = user[0][4]
                is_active = user[0][7]
                # check password correct
                if self._check_password(db_pass, password):
                    if is_active==True:
        
                        self.lt_instance.token_data = (user_ID,name,is_master_user) # using setter
                        token, front_end_token = self.lt_instance.login_token # getting token path & encrypted token for front end
                        
                        if token and front_end_token:
                            from backend_logic.user_backend import UserBackend
                            self.logger.log(self.class_name,'login', username, 'logged in')
                            facade=UserBackend(token) 
                            return (facade, err_msg, front_end_token)  # returning facade with the token path in init & encrypted token for front end
                    else:
                        self.logger.log(self.class_name,'login', username, err_msg)
                        err_msg= 'Your User Has Been Disactivated. Contact Customer Support For More Information.'
                        return (None, err_msg, None)
            else:
                self.logger.log(self.class_name,'login', username, err_msg)
                err_msg= 'Wrong Username/Passwod'
                return (None, err_msg, None)
            
        except Exception as e:
            self.logger.log(self.class_name,'login', username, str(e))
            return (None, str(e), None)
        
    
    def logout(self):
        try:
            self.lt_instance.delete_token_file()
            self.logger.log(self.class_name,'logout', None, 'logout sucsess')
            return True
        
        except Exception as e:
            self.logger.log(self.class_name,'logout', None, str(e))
            return False
        
            
    def add_user(self,*,username, password, email,
                 name, description):
        err_msg = None
        try:
            if self.users_repo.get_stored_procedure('check_if_user_exists',{'username':username, 'email':email}):
                err_msg = 'User with given email/username exists. Pick differernt email/username.'
                return (False,err_msg)
            
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                current_datetime = datetime.now()
                new_user = self.users_repo.add(Users(Username=username,PasswordHash=hashed_password,
                                                    Email=email, FullName=name, 
                                                    ProfileDescription=description, CreatedAt=current_datetime))
                if new_user:    # creation user sucsess
                    self.logger.log(self.class_name,'add_user', (username, email, name, description), True)
                    return (True, err_msg) 
                        
                else:   #user creation err
                    self.logger.log(self.class_name,'add_user', (username, email, name, description), err_msg)
                    err_msg = 'Error Signing Up. Try Again Later.'
                    return (False, err_msg)
                
        except Exception as e:
            self.logger.log(self.class_name,'add_user', (username, email, name, description), str(e))
            return (False,str(e))
    
    
    def format_datetime(self, date, time):
        combined_datetime_str = f"{date} {time}"
        try:
            formated_datetime = datetime.strptime(combined_datetime_str, '%d-%m-%Y %H:%M')
            self.logger.log(self.class_name,'format_datetime', (date,time), formated_datetime)
            return formated_datetime
        
        except Exception as e:
            self.logger.log(self.class_name,'format_datetime', (date,time), str(e))
            return None         
        
        
    def get_event_by_id (self, event_id):
        try:
            event=self.events_repo.get_by_id(event_id)
            if event:
                self.logger.log(self.class_name,'get_event_by_id', event_id, event)
                return event
            
            else:
                self.logger.log(self.class_name,'get_event_by_id', event_id, 'none found')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_event_by_id', event_id, str(e))
            return None

    
    def get_event_by_params (self, *, title, organiser, date, location, type):
        try:
            formatted_date= self.format_datetime(date,"00:00")
            events=self.events_repo.get_stored_procedure('get_event_by_params',{'title':title,
                                                                                'organiser':organiser,
                                                                                'date':formatted_date,
                                                                                'location':location,
                                                                                'type':type})
            if events:
                self.logger.log(self.class_name,'get_event_by_params', (title, organiser, date, location, type), events)
                return events
            
            else:
                self.logger.log(self.class_name,'get_event_by_params', (title, organiser, date, location, type), 'none found')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_event_by_id', (title, organiser, date, location, type), str(e))
            return None 
        
                
    def get_feedback_by_event (self, event_id):
        try:
            feedbacks=self.feedback_repo.get_stored_procedure('get_feedback_by_event',{'eventID':event_id})
            if feedbacks:
                self.logger.log(self.class_name,'get_feedback_by_event', event_id, feedbacks)
                return feedbacks
            
            else:
                self.logger.log(self.class_name,'get_feedback_by_event', event_id, 'none found')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_feedback_by_event', event_id, str(e))
            return None 
        

    def get_images_by_event (self, event_id):
        try:
            images=self.feedback_repo.get_stored_procedure('get_images_by_event',{'eventID':event_id})
            if images:
                self.logger.log(self.class_name,'get_images_by_event', event_id, images)
                return images
            
            else:
                self.logger.log(self.class_name,'get_images_by_event',event_id, 'none found')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_images_by_event', event_id, str(e))
            return None         

    
    def get_all_event_categories(self):
        try:
            categories= self.categories_repo.get_all()
            if categories:
                self.logger.log(self.class_name,'get_all_event_categories', None, categories)
                return categories
            
            else:
                self.logger.log(self.class_name,'get_all_event_categories', None, 'none found')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_all_event_categories', None, str(e))
            return None
        
        
    def get_category_by_id(self, category_id):
        try:
            category= self.categories_repo.get_by_id(category_id)
            if category:
                self.logger.log(self.class_name,'get_category_by_id', None, category)
                return category
            
            else:
                self.logger.log(self.class_name,'get_category_by_id', None, 'none found')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_category_by_id', None, str(e))
            return None
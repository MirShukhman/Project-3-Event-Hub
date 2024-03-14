
from app import bcrypt
from datetime import datetime

from backend_logic.backend_base import BackendBase
from backend_logic.authenticator import Authenticator

from modules.event_categories import EventCategories
from modules.event_images import EventImages
from modules.events import Events
from modules.feedback import Feedback
from modules.registrations import Registrations
from modules.users import Users

class UserBackend(BackendBase):
    def __init__(self, token_filepath):
        # Inherts FacadeBase init, 
        # LoginToken class instanse to acsess getter setter funcs from the class
        super().__init__()
        self.class_name=self.__class__.__name__
        self.authenticator = Authenticator(token_filepath)
        self.name = self.authenticator.get_user_fullname()
        self.id = self.authenticator.get_user_id()
        self.is_master = self.authenticator.get_master_approval()
        
    def _get_authentication(self,front_end_token):
        try:
            ok = self.authenticator.authenticate_user(front_end_token)
            if ok:
                self.logger.log(self.class_name,'_get_authentication', front_end_token, True)
                return True
            else:
                self.logger.log(self.class_name,'_get_authentication', front_end_token, False)
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'_get_authentication', front_end_token, str(e))
            return False 
        
           
    def get_user(self, front_end_token):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                user= self.users_repo.get_by_id(self.id)
                if user:
                    self.logger.log(self.class_name,'get_user', self.id, user)
                    return user

            else:
                self.logger.log(self.class_name,'get_user', (self.id,front_end_token), 'authentication fail/no user by id')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_user', (self.id,front_end_token), str(e))
            return None          
        
        
    def change_password(self, * ,front_end_token, old_pass, new_pass):
        err_msg = None
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                user=self.get_user(front_end_token)
                db_pass= user.PasswordHash
                if db_pass:
                    if self._check_password(db_pass, old_pass):
                        hashed_new_pass=bcrypt.generate_password_hash(new_pass).decode('utf-8')
                        update=self.users_repo.update(self.id,{'PasswordHash':hashed_new_pass})
                        if update:
                           return (True, err_msg)
                        else:
                            self.logger.log(self.class_name,'change_password', self.id, err_msg)
                            err_msg = 'Eror Updating. Try Again Later.'
                            return (False, err_msg)
                    else:
                        err_msg = 'Wrong Old Password.'
                        return (False, err_msg) 
            else:
                self.logger.log(self.class_name,'change_password', (self.id,front_end_token), err_msg)
                err_msg = 'Eror Updating. Try Again Later.'
                return (False, err_msg)
            
        except Exception as e:
            self.logger.log(self.class_name,'change_password', (self.id,front_end_token), str(e))
            return (False, str(e))
        
        
    def update_profile(self, * ,front_end_token, password, username,
                       email, fullname, profile_description):
        """
        27.02.24
        Mir Shukhman
        Update users profile, authenticates front end token against back end token using Authenticator class,
        calls get_user func to get users password from db, calls check_password from BackendBase class,
        calls check_if_user_exists sp to check if user with email or username given exists, and will with proceed
        with the update if either 1.user with such email and username dont exist; 
        or 2. if such user exists but it is the current user updating their own data.
        ;Logging of actions
        Input: front_end_token, password, username,email, fullname, profile_description
                [all params by name]
        Output: True; False
        """
        err_msg = None
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                user=self.get_user(front_end_token)
                db_pass= user.PasswordHash
                if db_pass:
                    if self._check_password(db_pass, password):
                        exists_with_credentials=self.users_repo.get_stored_procedure('check_if_user_exists',
                                                                                     {'username':username, 'email':email})
                        
                        if exists_with_credentials and exists_with_credentials[0][0] == self.id or not exists_with_credentials:
                            update=self.users_repo.update(self.id,{'Username':username,
                                                                    'Email':email,'FullName':fullname,
                                                                    'ProfileDescription':profile_description})
                            if update:
                                self.logger.log(self.class_name,'update_profile', self.id, 'update sucsess')
                                return (True, err_msg)
                            else:
                                self.logger.log(self.class_name,'update_profile', self.id, err_msg)
                                err_msg = 'Eror Updating. Try Again Later.'
                                return (False, err_msg)
                                   
                        else:
                            err_msg = 'User with given email/username exists. Pick differernt email/username.'
                            return (False,err_msg)
                    else:
                        err_msg = 'Wrong Old Password.'
                        return (False,err_msg)
                    
            else:
                self.logger.log(self.class_name,'update_profile', (self.id,front_end_token), err_msg)
                err_msg = 'Eror Updating. Try Again Later.'
                (False,err_msg)
            
        except Exception as e:
            self.logger.log(self.class_name,'update_profile', (self.id,front_end_token), str(e))
            return (False, str(e)) 
     
        
    def my_events(self, front_end_token):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                my_events= self.events_repo.get_stored_procedure('get_my_events',{'organiserID':self.id})
                if my_events:
                    self.logger.log(self.class_name,'my_events', (self.id,front_end_token), my_events)
                    return my_events
                else:
                    self.logger.log(self.class_name,'my_events', (self.id,front_end_token), 'None found')
                    return None
                
            else:
                self.logger.log(self.class_name,'my_events', (self.id,front_end_token), 'authentication fail')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'my_events', (self.id,front_end_token), str(e))
            return None          
        
            
    def add_event(self, * ,front_end_token, title, description, 
                  location, date, time, image, cathegory_id, is_private):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                datetime=self.format_datetime(date,time)
                new_event= self.events_repo.add(Events(Title=title,Description=description,
                                                       Location=location,EventDateTime=datetime,
                                                       EventImage=image,OrganizerID=self.id,
                                                       CategoryID=cathegory_id,IsPrivate=is_private))
                if new_event:
                    self.logger.log(self.class_name,'add_event', (front_end_token, title, description, 
                  location, date, time, image, cathegory_id, is_private), 'event added')
                    return True
                
            else:
                self.logger.log(self.class_name,'add_event', (self.id, front_end_token, title, description, 
                  location, date, time, image, cathegory_id, is_private), 'authentication fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'add_event', (self.id,front_end_token), str(e))
            return False 
        
        
    def update_event(self,*, front_end_token,event_id, title, description, 
                  location, date, time, image, cathegory_id, is_private):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                event = self.events_repo.get_by_id(event_id)
                if event and event.OrganizerID == self.id:
                    datetime=self.format_datetime(date,time)
                    updated_event= self.events_repo.update(event_id,{'Title':title,'Description':description,
                                                        'Location':location,'EventDateTime':datetime,
                                                        'EventImage':image,'OrganizerID':self.id,
                                                        'CategoryID':cathegory_id,'IsPrivate':is_private})
                    if updated_event:
                        self.logger.log(self.class_name,'update_event', (front_end_token, event_id, title, description, 
                            location, date, time, image, cathegory_id, is_private), 'event updated')
                        return True
                    
            else:
                self.logger.log(self.class_name,'update_event', (self.id,front_end_token),
                                'authentication fail/userId != organiser id/No event found/update event err')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'update_event', (self.id,front_end_token), str(e))
            return False  
        
        
    def cancel_event(self, front_end_token,event_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                event = self.events_repo.get_by_id(event_id)
                if event and event.OrganizerID == self.id:
                    cancel_event= self.events_repo.update(event_id,{'IsCanceled':True})
                    
                    if cancel_event:
                        self.logger.log(self.class_name,'cancel_event', (front_end_token, event_id), 'event canceled')
                        return True
                    
            else:
                self.logger.log(self.class_name,'cancel_event', (self.id,front_end_token),
                                'authentication fail/userId != organiser id or No event found/event canceled')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'cancel_event', (self.id,front_end_token), str(e))
            return False  
                 

    def get_registrations_by_event (self, front_end_token, event_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                my_events= self.my_events(front_end_token)
                for event in my_events:
                    if event[6] == self.id:
                        registrations=self.feedback_repo.get_stored_procedure('get_registrations_by_event',{'eventID':event_id})
                        if registrations:
                            self.logger.log(self.class_name,'get_registrations_by_event', (event_id,front_end_token), registrations)
                            return registrations
                
            else:
                self.logger.log(self.class_name,'get_registrations_by_event',(front_end_token,event_id), 'authentication fail/none found/not organiser')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_registrations_by_event', (front_end_token,event_id), str(e))
            return None 
        
    
    def my_registrations(self, front_end_token):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                registrations=self.events_repo.get_stored_procedure('get_my_registrations',{'atendieeID':self.id})
                if registrations:
                    self.logger.log(self.class_name,'my_registrations', (self.id,front_end_token), registrations)
                    return registrations
                
                else:
                    self.logger.log(self.class_name,'my_registrations', (self.id,front_end_token), 'None found')
                    return None
            
            else:
                self.logger.log(self.class_name,'my_registrations', (self.id,front_end_token), 'authentication fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'my_registrations', (self.id,front_end_token), str(e))
            return False 
            
       
    def register_to_event(self, front_end_token,event_id):
        err_msg= None
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                event=self.events_repo.get_by_id(event_id)
                if event and event.IsCanceled==False:
                    is_registered= self.events_repo.get_stored_procedure('check_if_registered',
                                                                         {'userID':self.id,'eventID':event_id})
                    if is_registered:
                        err_msg= "You Are Already Registered for the Event!"
                        return (False, err_msg)
                    
                    status = 'Pending Approval' if event.IsPrivate else "Approved"
                    current_datetime = datetime.now()
                    registration= self.registrations_repo.add(Registrations(EventID=event_id,UserID=self.id,
                                                                            RegistrationDateTime=current_datetime,
                                                                            Status=status))
                    if registration:
                        self.logger.log(self.class_name,'register_to_event', (self.id,front_end_token,event_id),
                                        (status,'registered'))
                        return (status, err_msg)
                    else:
                        self.logger.log(self.class_name,'register_to_event', (self.id,front_end_token,event_id), err_msg)
                        err_msg = 'Eror Registering to the Event. Try Again Later.'
                        return (False, err_msg)
                else:
                    self.logger.log(self.class_name,'register_to_event', (self.id,front_end_token,event_id), err_msg)
                    err_msg = 'The event You wish to Register for is Canceled or Does Not Exist.'
                    return (False, err_msg)
            else:
                self.logger.log(self.class_name,'register_to_event', (self.id,front_end_token), err_msg)
                err_msg = 'Eror Registering to the Event. Try Again Later.'
                return (False, err_msg)
            
        except Exception as e:
            self.logger.log(self.class_name,'register_to_event', (self.id,front_end_token), str(e))
            return (False, str(e))
        
        
    def cancel_registration_to_event(self, front_end_token, event_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                registrations= self.my_registrations(front_end_token)
                if registrations:
                    for registration in registrations:
                        if registration.EventID == event_id:
                            cancel = self.registrations_repo.remove(registration.RegistrationID)
                            if cancel:
                                return True
            else:
                self.logger.log(self.class_name,'cancel_registration_to_event', (self.id,front_end_token,event_id),
                                'authentication fail/no registration/cancel fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'cancel_registration_to_event', (self.id,front_end_token), str(e))
            return False 
        
        
    def decline_registration(self,front_end_token, registration_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                registration = self.registrations_repo.get_by_id(registration_id)
                event = self.events_repo.get_by_id(registration.EventID)
                if event.OrganizerID == self.id and event.IsPrivate:
                    decline = self.registrations_repo.update(registration_id,{'Status': 'Declined'})
                    if decline:
                        return True
            else:
                self.logger.log(self.class_name,'decline_registration', (self.id,front_end_token,registration_id),
                                'authentication fail/no registration/decline fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'decline_registration', (self.id,front_end_token), str(e))
            return False 
        
        
    def approve_registration(self,front_end_token, registration_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                registration = self.registrations_repo.get_by_id(registration_id)
                event = self.events_repo.get_by_id(registration.EventID)
                if event.OrganizerID == self.id and event.IsPrivate:
                    approve = self.registrations_repo.update(registration_id,{'Status': 'Approved'})
                    if approve:
                        return True
            else:
                self.logger.log(self.class_name,'approve_registration', (self.id,front_end_token,registration_id),
                                'authentication fail/no registration/approve fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'approve_registration', (self.id,front_end_token), str(e))
            return False 
        
        
    def add_feedback(self, *,front_end_token, event_id, raiting, comment):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                event = self.events_repo.get_by_id(event_id)
                current_datetime = datetime.now()
                event_datetime = event.EventDateTime
                if event_datetime < current_datetime and not event.IsCanceled:
                    registrations = self.my_registrations(front_end_token)
                    for registration in registrations:
                        if registration[1] == event_id and registration[4] == 'Approved':
                            feedback = self.feedback_repo.add(Feedback(RegistrationID= registration[0],
                                                                    Raiting=raiting, Comment=comment,
                                                                    SubmittionDateTime= current_datetime))
                            if feedback:
                                self.logger.log(self.class_name,'add_feedback', (self.id,front_end_token
                                                                                 ,event_id,raiting,comment), 'feedback added')
                                return True
                            
            else:
                self.logger.log(self.class_name,'add_feedback', (self.id,front_end_token,event_id), 
                                'authentication fail/event is yet to happen/canceled/adding fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'add_feedback', (self.id,front_end_token), str(e))
            return False 
        
        
    def update_feedback(self, *,front_end_token, feedback_id, raiting, comment):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                feedback= self.feedback_repo.get_by_id(feedback_id)
                my_registrations= self.my_registrations
                for registration in my_registrations:
                    if registration[0] == feedback.RegistrationID:
                        current_datetime = datetime.now()
                        update_feedback = self.feedback_repo.update(feedback_id,{'Raiting':raiting, 'Comment':comment,
                                                                                'SubmittionDateTime':current_datetime})
                        if update_feedback:
                            self.logger.log(self.class_name,'update_feedback', (self.id,front_end_token,feedback_id,raiting,comment),
                                            'updated')
                            return True
            else:
                self.logger.log(self.class_name,'update_feedback', (self.id,front_end_token,feedback_id), 
                                'authentication fail/update fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'update_feedback', (self.id,front_end_token), str(e))
            return False 
        
        
    def delete_feedback(self,front_end_token, feedback_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                feedback= self.feedback_repo.get_by_id(feedback_id)
                my_registrations= self.my_registrations
                for registration in my_registrations:
                    if registration[0] == feedback.RegistrationID:
                        delete_feedback = self.feedback_repo.remove(feedback_id)
                        if delete_feedback:
                            self.logger.log(self.class_name,'delete_feedback', (self.id,front_end_token,feedback_id), 'removed')
                            return True
            else:
                self.logger.log(self.class_name,'delete_feedback', (self.id,front_end_token,feedback_id), 'authentication fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'delete_feedback', (self.id,front_end_token), str(e))
            return False 
        
        
    def add_event_image_attendee(self, *,front_end_token, event_id, image):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                event = self.events_repo.get_by_id(event_id)
                current_datetime = datetime.now()
                event_datetime = event.EventDateTime
                if event_datetime < current_datetime and not event.IsCanceled:
                    registrations = self.my_registrations(front_end_token)
                    for registration in registrations:
                        if registration[1] == event_id and registration[4] == 'Approved':
                            add_image = self.images_repo.add(EventImages(EventID=event_id,
                                                                         Image=image,UserID=self.id,
                                                                         SubmittionDateTime=current_datetime))
                            if add_image:
                                self.logger.log(self.class_name,'add_event_image_attendee', (self.id,front_end_token
                                                                                 ,event_id), 'image added')
                                return True
                            
            else:
                self.logger.log(self.class_name,'add_event_image_attendee', (self.id,front_end_token,event_id), 
                                'authentication fail/event is yet to happen/canceled/adding fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'add_event_image_attendee', (self.id,front_end_token), str(e))
            return False
        
        
    def add_event_image_organiser(self, *,front_end_token, event_id, image):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                event = self.events_repo.get_by_id(event_id)
                current_datetime = datetime.now()
                event_datetime = event.EventDateTime
                if event_datetime < current_datetime and not event.IsCanceled and event.OrganizerID == self.id:
                    add_image = self.images_repo.add(EventImages(EventID=event_id,
                                                                    Image=image,UserID=self.id,
                                                                    SubmittionDateTime=current_datetime))
                    if add_image:
                        self.logger.log(self.class_name,'add_event_image_organiser', (self.id,front_end_token
                                                                            ,event_id),  'image added')
                        return True
                            
            else:
                self.logger.log(self.class_name,'add_event_image_organiser', (self.id,front_end_token,event_id), 
                                'authentication fail/event is yet to happen/canceled/adding fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'add_event_image_organiser', (self.id,front_end_token), str(e))
            return False
        
        
    def delete_image(self,front_end_token, image_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok:
                image = self.images_repo.get_by_id(image_id)
                if image.UserID == self.id:
                    delete= self.images_repo.remove(image_id)
                    if delete:
                        self.logger.log(self.class_name,'delete_image', (self.id,front_end_token,image_id), 'deleted')
                        return True
            else:
                self.logger.log(self.class_name,'delete_image', (self.id,front_end_token,image_id), 'authentication fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'delete_image', (self.id,front_end_token), str(e))
            return False 
        
        
    # Master Functionality
    
    def add_master_user(self,front_end_token, user_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master:
                set_as_master = self.users_repo.update(user_id,{'IsMasterUser':True})
                if set_as_master:
                    self.logger.log(self.class_name,'add_master_user', (self.id,front_end_token,user_id), 'sucsess')
                    return True
                
            else:
                self.logger.log(self.class_name,'add_master_user', (self.id,front_end_token,user_id), 'authentication/add_master fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'add_master_user', (self.id,front_end_token), str(e))
            return False         
        
   
    def remove_master_user(self,front_end_token, user_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master:
                remove_master = self.users_repo.update(user_id,{'IsMasterUser':False})
                if remove_master:
                    self.logger.log(self.class_name,'remove_master_user', (self.id,front_end_token,user_id), 'sucsess')
                    return True
                
            else:
                self.logger.log(self.class_name,'remove_master_user', (self.id,front_end_token,user_id), 'authentication/remove_master_user fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'remove_master_user', (self.id,front_end_token), str(e))
            return False
        
         
    def disactivate_user(self,front_end_token, user_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master and self.id != user_id:
                disactivate = self.users_repo.update(user_id,{'IsActive':False})
                if disactivate:
                    self.logger.log(self.class_name,'disactivate_user', (self.id,front_end_token,user_id), 'disactivated')
                    return True
                
            else:
                self.logger.log(self.class_name,'disactivate_user', 
                                (self.id,front_end_token,user_id), 'authentication/disactivate fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'disactivate_user', (self.id,front_end_token), str(e))
            return False      
   
        
    def reactivate_user(self,front_end_token, user_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master and self.id != user_id:
                reactivate = self.users_repo.update(user_id,{'IsActive':True})
                if reactivate:
                    self.logger.log(self.class_name,'reactivate_user', (self.id,front_end_token,user_id), 'reactivated')
                    return True
                
            else:
                self.logger.log(self.class_name,'reactivate_user', 
                                (self.id,front_end_token,user_id), 'authentication/reactivate fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'reactivate_user', (self.id,front_end_token), str(e))
            return False 
      
      
    def get_user_by_id(self,front_end_token, user_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master:
                user= self.users_repo.get_by_id(user_id)
                if user:
                    self.logger.log(self.class_name,'get_user_by_id', (self.id,front_end_token,user_id), user)
                    return user             
            else:
                self.logger.log(self.class_name,'get_user_by_id', (self.id,front_end_token,user_id), 'authentication fail/none found')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_user_by_id', (self.id,front_end_token), str(e))
            return None 
        
          
    def get_all_events(self,front_end_token):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master:
                all_events= self.events_repo.get_all()
                if all_events:
                    self.logger.log(self.class_name,'get_all_events', (self.id,front_end_token), all_events)
                    return all_events             
            else:
                self.logger.log(self.class_name,'get_all_events', (self.id,front_end_token), 'authentication fail/none found')
                return None
            
        except Exception as e:
            self.logger.log(self.class_name,'get_all_events', (self.id,front_end_token), str(e))
            return None 
        
               
    def add_category(self, *, front_end_token, category, description):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master:
                new_category = self.categories_repo.add(EventCategories(EventCategory=category,
                                                                        Description=description))
                if new_category:
                    self.logger.log(self.class_name,'add_category',
                                    (self.id,front_end_token,category,description), 'added')
                    return True
                
            else:
                self.logger.log(self.class_name,'add_category', (self.id,front_end_token), 'authentication/adding fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'add_category', (self.id,front_end_token), str(e))
            return False 
        
        
    def update_category(self, *, front_end_token, category_id, category, description):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master:
                update = self.categories_repo.update(category_id,{'EventCategory':category,
                                                                  'Description':description})
                if update:
                    self.logger.log(self.class_name,'update_category',
                        (self.id,front_end_token,category_id,category,description), 'updated')
                    return True
                             
            else:
                self.logger.log(self.class_name,'update_category', (self.id,front_end_token, category_id), 'authentication/update fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'update_category', (self.id,front_end_token), str(e))
            return False 
        
        
    def delete_category(self, front_end_token, category_id):
        try:
            ok = self._get_authentication(front_end_token)
            if ok and self.is_master:
                delete = self.categories_repo.remove(category_id)
                if delete:
                    self.logger.log(self.class_name,'delete_category',
                        (self.id,front_end_token,category_id), 'deleted')
                    return True
                             
            else:
                self.logger.log(self.class_name,'delete_category', (self.id,front_end_token,category_id), 'authentication/delete fail')
                return False
            
        except Exception as e:
            self.logger.log(self.class_name,'delete_category', (self.id,front_end_token), str(e))
            return False 
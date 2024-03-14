
from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from backend_logic.backend_base import BackendBase
from backend_logic.user_backend import UserBackend

class Routes(Blueprint):
    def __init__(self, name, import_name):
        super().__init__(name, import_name)
        self.route('/login', methods=['POST'])(self.login)
        self.route('/signup', methods=['POST'])(self.signup)
        self.route('/logout', methods=['POST'])(self.logout)
        self.route('/my_events', methods=['POST'])(self.my_events)
        self.route('/add_event', methods=['POST'])(self.add_event)
        self.route('/get_categories', methods=['GET'])(self.get_categories)
        # Master User
        self.route('/all_events', methods=['POST'])(self.all_events)
        self.backend_base = BackendBase()
        self._facade= None
        
    @property
    def facade(self):
        return self._facade
     
    @facade.setter
    def facade(self, new_facade):
        self._facade = new_facade
        
    def login(self):
        try:
            data= request.json
            if not data:
                return jsonify({'error': 'Incomplete or no data provided for login'}), 400
            
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({'error': 'Incomplete or no data provided for login'}), 400

            user_facade, err, front_end_token = self.backend_base.login(username=username, password=password)           
            
            if err:
                return jsonify({'error': err}), 401
            
            if user_facade and front_end_token:
                self.facade = user_facade
                name = self.facade.name
                is_master= self.facade.is_master
                return jsonify({'front_end_token':front_end_token,'users_name':name,'is_master':is_master}), 201

        except Exception as e:
            return jsonify({'error':str(e)}), 500
      
        
    def signup(self):
        try:
            data= request.json
            if not data:
                return jsonify({'error': 'Incomplete or no data provided for signup'}), 400
            
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            name = data.get('name')
            description = data.get('description')

            if not username or not password or not email or not name:
                return jsonify({'error': 'Incomplete or no data provided for signup'}), 400

            add, err = self.backend_base.add_user(username=username, password=password,
                                                  email=email, name=name, description=description)           
            
            if err:
                return jsonify({'error': err}), 400
            
            if add:
                return jsonify({'signup':add}), 201

        except Exception as e:
            return jsonify({'error':str(e)}), 500
        
    
    def logout(self):
        try:
            logout = self.backend_base.logout()
            if logout:
                self.facade = None
                return jsonify({'logged_out':logout}), 201
            else:
                return jsonify({'logged_out': logout}), 400

        except Exception as e:
            return jsonify({'error':str(e)}), 500
        
    
    def my_events(self):
        try:
            data= request.json
            if not data:
                return jsonify({'error': 'Incomplete or no data provided'}), 400
            
            front_end_token = data.get('token')
            if not front_end_token:
                return jsonify({'error': 'Authentication Error'}), 401
            
            my_events = self.facade.my_events(front_end_token)
            if my_events: 
                converted_events = []
                for event in my_events:
                    converted_events.append({
                        'event_id': event[0],
                        'title': event[1],
                        'description': event[2],
                        'location': event[3],
                        'date': event[4].strftime('%Y-%m-%d') if event[4] is not None else None,
                        'time': event[4].strftime('%H:%M:%S') if event[4] is not None else None,
                        'image': event[5].isoformat() if event[5] is not None else None,
                        'organizer': event[6],
                        'category': event[7],
                        'is_private': event[8],
                        'is_canceled': event[9]
                    })  
                    
                return jsonify({'my_events':converted_events}), 201
            
            else:
                return jsonify({'my_events':None}), 201

        except Exception as e:
           return jsonify({'error':str(e)}), 500 
       
       
    def add_event(self):
        try:
            data= request.json
            if not data:
                return jsonify({'error': 'Incomplete or no data provided'}), 400
            
            front_end_token = data.get('token')
            if not front_end_token:
                return jsonify({'error': 'Authentication Error'}), 401
            
            title = data.get('title')
            description = data.get('description')
            location = data.get('location')
            date = data.get('date')
            time = data.get('time')
            image = data.get('image')
            category = data.get('category')
            is_private = data.get('isPrivate')
            
            add = self.facade.add_event(front_end_token=front_end_token, title=title, 
                                        description=description, location=location,
                                        date=date, time=time, image=image, 
                                        cathegory_id=category, is_private=is_private)
            
            if add:  
                return jsonify({'add_event':add}), 201
            
            else:
                return jsonify({'error':'Authentication Error'}), 401

        except Exception as e:
           return jsonify({'error':str(e)}), 500 
       
       
    def get_categories(self):
        try:         
            categories = self.backend_base.get_all_event_categories()
            
            if categories: 
                converted_categories = []
                for category in categories:
                    converted_categories.append({
                        'category_id': category.CategoryID,
                        'category': category.EventCategory,
                        'description': category.Description,
                    })  
                    
                return jsonify({'categories':converted_categories}), 201
            
            else:
                return jsonify({'error':'Authentication Error'}), 401

        except Exception as e:
           return jsonify({'error':str(e)}), 500 
        
        
    def all_events(self):
        try:
            data= request.json
            if not data:
                return jsonify({'error': 'Incomplete or no data provided'}), 400
            
            front_end_token = data.get('token')
            if not front_end_token:
                return jsonify({'error': 'Authentication Error'}), 401
            
            all_events = self.facade.get_all_events(front_end_token)
            if all_events: 
                converted_events = []
                for event in all_events:
                    categoty_name = self.backend_base.get_category_by_id(event.CategoryID)
                    organizer = self.facade.get_user_by_id(front_end_token,event.OrganizerID)
                    converted_events.append({
                        'event_id': event.EventID,
                        'title': event.Title,
                        'description': event.Description,
                        'location': event.Location,
                        'date': event.EventDateTime.strftime('%Y-%m-%d') if event.EventDateTime is not None else None,
                        'time': event.EventDateTime.strftime('%H:%M:%S') if event.EventDateTime is not None else None,
                        'image': event.EventImage.isoformat() if event.EventImage is not None else None,
                        'organizer_id': event.OrganizerID,
                        'organizer_name': organizer.FullName,
                        'category': categoty_name.EventCategory,
                        'is_private': event.IsPrivate,
                        'is_canceled': event.IsCanceled
                    })  
                    
                return jsonify({'all_events':converted_events}), 201
            
            else:
                return jsonify({'all_events':None}), 201

        except Exception as e:
           return jsonify({'error':str(e)}), 500 
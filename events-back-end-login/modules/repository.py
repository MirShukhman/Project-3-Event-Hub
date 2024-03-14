
from sqlalchemy import text

from modules import db
from logger import Logger

# Instance of logger to acsess the log func from Logger class
logger = Logger()

# 24.02.24
# Mir Shukhman
# Defining class Repository wich will hold all CRUD funcs for db.Models 
#       and func acsessing and executing the Stored Procedures saved in the db.
# Every use of one of Repo's funcs will be logged in 'log.json' in format:
#       id(Auto-generated), dattime(Auto-generated), class_name, func_name, func_input, func_output

class Repository:
    def __init__(self, model):
        """
        24.02.24
        Mir Shukhman
        Input: db.Model (table) as object
        """
        self.model = model
        self.class_name = str(model)

    # CRUD funcs for all db.Models
    
    def get_by_id(self, entity_id):
        """
        24.02.24
        Mir Shukhman
        Getting entity by entity's ID
        Input: entity ID (int)
        Output: entity (db.model object); None if not found or err;
        ;logging of action
        """
        try:
            result = self.model.query.get(entity_id)
            if result:
                logger.log(self.class_name,'get_by_id', entity_id, result)
                return result
            else:
                logger.log(self.class_name,'get_by_id', entity_id, 'None found')
                return None
        
        except Exception as e:
            logger.log(self.class_name,'get_by_id', entity_id, str(e))
            return None


    def get_all(self):
        """
        24.02.24
        Mir Shukhman
        Getting all entities of certain table in db(class db.model)
        Input: None
        Output: all class objects al list of db.model obj; None if not found or err;
        ;logging of action
        """
        try:
            result = self.model.query.all()
            if result:
                logger.log(self.class_name,'get_all', 'None', str(result))
                return result
            else:
                logger.log(self.class_name,'get_all', 'None', 'None Found')
                return None
            
        except Exception as e:
            logger.log(self.class_name,'get_all', 'None', str(e))
            return None


    def add(self, entity):
        """
        24.02.24
        Mir Shukhman
        Adding new entity to certain table in db (class db.model)
        Input: entity to add as in 
                Users(Username='x', Password='y', Email='z', UserRole=1)
        Output: True if action sucsess; None if err;
        ;logging of action
        """
        try:
            db.session.add(entity)
            db.session.commit()
            logger.log(self.class_name,'add', entity, 'Added')
            return True # Return sucsess of action
            
        except Exception as e:
            db.session.rollback()
            logger.log(self.class_name,'add', entity, str(e))
            return None


    def update(self, entity_id, new_info):
        """
        24.02.24
        Mir Shukhman
        Updating an existing entity to certain table in db (class db.model)
        First calls get_by_id func from the class to find the entity,
            then if entity found updates.
        Input: entity_id (int),
            new_info - Dictionary of parameter names and values as in {'Username': 'new_username'}
        Output: True is sucsess; None if not found or err;
        ;logging of action
        """
        try:
            entity = self.get_by_id(entity_id)
            
            if entity:
                for key, value in new_info.items():
                    setattr(entity, key, value)  
                db.session.commit()
                logger.log(self.class_name,'update', (entity_id, new_info), 'Updated')
                return True  # Return sucsess of action
                
            else:
                logger.log(self.class_name,'update', (entity_id, new_info), 'None Found')
                return None
        
        except Exception as e:
            db.session.rollback()
            logger.log(self.class_name,'update', (entity_id, new_info), str(e))
            return None
        

    def remove(self, entity_id):
        """
        24.02.24
        Mir Shukhman
        Removing an existing entity to certain table in db (class db.model)
        First calls get_by_id func from the class to find the entity,
            then if entity found deletes.
        Input: entity ID (int)
        Output: True if found and delted; None if not found or err;
        ;logging of action
        """
        try:
            entity = self.get_by_id(entity_id)
            
            if entity:
                db.session.delete(entity) 
                db.session.commit()
                logger.log(self.class_name,'remove', entity_id, 'Removed')
                return True  # Return sucsess of action
                
            else:
                logger.log(self.class_name,'remove', entity_id, 'None Found')
                return None
        
        except Exception as e:
            db.session.rollback()
            logger.log(self.class_name,'remove', entity_id, str(e))
            return None


    # Func calling for pre-created Stored Procedurs in SQL db
    
    def get_stored_procedure(self, sp_name, parameters):
        """
        24.02.24
        Mir Shukhman
        Universal function for executing stored procedures in the db
        Input: sp_name - Name of the stored procedure (str)
            parameters - Dictionary of parameter names and values as in {"UserID":345}
        Output: returns stored procedure's output; None if not found or err;
        ;logging of action
        """
        try:
            query = text(f"EXEC {sp_name} " + ", ".join([f":{param}" for param in parameters.keys()]))
            
            result = db.session.execute(query, parameters)
            result_set = result.fetchall()
            
            if result_set:
                logger.log(self.class_name, sp_name, parameters, result_set)
                return result_set
            else:
                logger.log(self.class_name, sp_name, parameters, 'None Found')
                return None

        except Exception as e:
            logger.log(self.class_name, sp_name, parameters, str(e))
            return None
        

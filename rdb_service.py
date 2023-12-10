import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import create_database, Base, BaseInformation
from config import ConfigParser
import uuid

class DatabaseAgent:
    def __init__(self) -> None:
        self.config = ConfigParser()

    def init_connection_db(self):
        USERNAME = self.config.get(key='mysql_database')['user_name']
        PASSWORD = self.config.get(key='mysql_database')['password']
        SERVER = self.config.get(key='mysql_database')['server']
        DBNAME = self.config.get(key='mysql_database')['dbname']

        DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{SERVER}:3306/{DBNAME}"

        try:
            engine = create_engine(DATABASE_URL)
            connection = engine.connect()
            connection.close()
        except:
            create_database(SERVER, USERNAME, PASSWORD, DBNAME)
            engine = create_engine(DATABASE_URL)

        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        Session = session()
        self.session = Session
        self.user_uuid = str(uuid.uuid4())
        return Session

    def create_new_user(self):
        new_user = BaseInformation(user_uuid=self.user_uuid)
        self.session.add(new_user)
        self.session.commit()
        return self.user_uuid        

    def check_missing_fields(self, user_uuid):
        user = self.session.query(BaseInformation).filter_by(user_uuid=user_uuid).first()

        if not user:
            return f"No user found with user_id {user_uuid}"

        missing_fields = []
        for field in BaseInformation.__table__.columns:
            if getattr(user, field.name) is None:
                missing_fields.append(field.name)
        
        return missing_fields if missing_fields else "No missing fields"

    @staticmethod
    def add_scores(session, user_uuid, args_dict):
        ielt, toelf, gpa = None, None, None
        if args_dict["ielt"]:
            ielt = float(args_dict["ielt"])

        if args_dict["toelf"]:
            toelf = int(args_dict["toelf"])

        if args_dict["gpa"]:
            gpa = float(args_dict["gpa"])

        user = session.query(BaseInformation).filter_by(user_uuid=user_uuid).first()
        if user:
            user.eng_ielts = ielt if ielt else user.eng_ielts
            user.eng_toelf = toelf if toelf else user.eng_toelf
            user.score_gpa = gpa if gpa else user.score_gpa
            session.commit()
            return None
        else:
            return f"No user found with user_id {user_uuid}"
    
    # @staticmethod
    # def add_gpa(session, user_uuid, args_dict):
    #     if args_dict["gpa"]:
    #         gpa = float(args_dict["gpa"])

    #     user = session.query(BaseInformation).filter_by(user_uuid=user_uuid).first()

    #     if user:
    #         user.score_gpa = gpa if gpa else user.score_gpa
    #         session.commit()
    #     else:
    #         return f"No user found with user_id {user_uuid}"

    @staticmethod
    def add_target_infor(session, user_uuid, args_dict):
        trg_country, trg_uni, trg_major, trg_job, budget = None, None, None, None, None

        if "trg_country" in args_dict and args_dict["trg_country"]:
            trg_country = args_dict["trg_country"]

        if "trg_uni" in args_dict and args_dict["trg_uni"]:
            trg_uni = args_dict["trg_uni"]

        if "trg_major" in args_dict and args_dict["trg_major"]:
            trg_major = args_dict["trg_major"]
                                  
        if "trg_job" in args_dict and args_dict["trg_job"]:
            trg_job = args_dict["trg_job"]

        if "budget" in args_dict and args_dict["budget"]:
            budget = args_dict["budget"]

        user = session.query(BaseInformation).filter_by(user_uuid=user_uuid).first()

        if user:
            user.target_country = trg_country if trg_country else user.target_country
            user.target_university = trg_uni if trg_uni else user.target_university
            user.target_major = trg_major if trg_major else user.target_major
            user.target_job = trg_job if trg_job else user.target_job
            user.budget = budget if budget else user.budget
            session.commit()
            return None
        else:
            return f"No user found with user_id {user_uuid}"

    def get_all_infor(self, user_uuid):
        return self.session.query(BaseInformation).filter(BaseInformation.user_uuid == user_uuid).first()
        
    # @staticmethod
    # def add_target_university(session, user_uuid, args_dict):
    #     if args_dict["trg_uni"]:
    #         trg_uni = args_dict["trg_uni"]

    #     user = session.query(BaseInformation).filter_by(user_uuid=user_uuid).first()

    #     if user:
    #         user.target_university = trg_uni if trg_uni else user.target_university
    #         session.commit()
    #     else:
    #         return f"No user found with user_id {user_uuid}"
    
    # @staticmethod
    # def add_target_major(session, user_uuid, args_dict):
    #     if args_dict["trg_major"]:
    #         trg_major = args_dict["trg_major"]

    #     user = session.query(BaseInformation).filter_by(user_uuid=user_uuid).first()

    #     if user:
    #         user.target_major = trg_major if trg_major else user.target_major
    #         session.commit()
    #     else:
    #         return f"No user found with user_id {user_uuid}"
    
    # @staticmethod
    # def add_target_job(session, user_uuid, args_dict):
    #     if args_dict["trg_job"]:
    #         trg_job = args_dict["trg_job"]

    #     user = session.query(BaseInformation).filter_by(user_id=user_uuid).first()

    #     if user:
    #         user.target_job = trg_job if trg_job else user.target_job
    #         session.commit()
    #     else:
    #         return f"No user found with user_id {user_uuid}"

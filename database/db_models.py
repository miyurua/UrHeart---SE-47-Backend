from mongoengine import DateTimeField
from .db import db
import datetime


class Patient(db.Document):
    age = db.FloatField(required=True)
    sex = db.FloatField(required=True)
    chest_pain_type = db.FloatField(required=True)
    resting_blood_pressure = db.FloatField(required=True)
    cholesterol_level = db.FloatField(required=True)
    fasting_blood_sugar_level = db.FloatField(required=True)
    rest_ecg = db.FloatField(required=True)
    max_heart_rate_achieved = db.FloatField(required=True)
    exercise_induced_angina = db.FloatField(required=True)
    st_slope = db.FloatField(required=True)
    num_major_vessels = db.FloatField(required=True)

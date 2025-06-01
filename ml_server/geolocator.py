import spacy
from geopy.geocoders import Nominatim

nlp = spacy.load("en_core_web_sm")
geo = Nominatim(user_agent="crime-geolocator")

def extract_location(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            location = geo.geocode(ent.text)
            if location:
                return location
    return None

import spacy

# Load spaCy model globally to avoid reloading
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Download the model if it's not already installed
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Entity Label to Full Form Mapping
ENTITY_FULL_FORMS = {
    "ORG": "Organization",
    "PERSON": "Person",
    "GPE": "Geopolitical Entity",
    "LOC": "Location",
    "DATE": "Date",
    "TIME": "Time",
    "MONEY": "Monetary Value",
    "PERCENT": "Percentage",
    "CARDINAL": "Cardinal Number",
    "NORP": "Nationalities or Religious/Political Groups",
    "FAC": "Facility",
    "LAW": "Law",
    "PRODUCT": "Product",
    "EVENT": "Event",
    "WORK_OF_ART": "Work of Art",
    "LANGUAGE": "Language",
    "QUANTITY": "Quantity",
}

def extract_named_entities_with_full_forms(text):
    """
    Extract named entities and their labels with full forms.
    """
    doc = nlp(text)
    entities = [
        (ent.text, ent.label_, ENTITY_FULL_FORMS.get(ent.label_, "Unknown"))
        for ent in doc.ents
    ]
    return entities

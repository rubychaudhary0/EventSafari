import pickle
import os

def load_recommendation_model():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'event_list.pkl')
    
    with open(file_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

    file = os.path.join(os.path.dirname(__file__), 'data', 'similarity.pkl')
    with open(file, 'rb') as model_file:
        modell = pickle.load(model_file)
    return modell

    
similarity = pickle.load(open('similarity.pkl','rb'))
#print(similarity)
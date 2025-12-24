from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal,Optional
import json
import pickle
import pandas as pd 


# create an instance of FastAPI
app = FastAPI()


# Patient model 
class Patient(BaseModel):
    id:Annotated[str,Field(...,max_length=50,title="id of the patient",example="P001")]
    name:Annotated[str,Field(...,max_length=50,title="name of the patient",description="name of the patient should be less than 50 characters")]
    city:Annotated[str,Field(...,title="city name of the patient",description="name of the patient should be less than 50 characters")]
    age:Annotated[int,Field(...,gt=0,lt=120,title="age of the patient",description="age of the patient should be 0 to 120")]
    gender:Annotated[Literal['male','female','others'],Field(...,title="gender of the patient",description="height of the patient should be Male or Female")]
    weight:Annotated[float,Field(...,gt=0,title="weight of the patient",description="weight of the patient should be greater than 0")]
    height:Annotated[float,Field(...,gt=0,title="height of the patient",description="height of the patient should be greater than 0")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if(self.bmi<18.5):
            return "Underweight"
        elif(self.bmi<30):
            return "Normal"
        else:
            return "Obese"



class Patient2(BaseModel):
    id:Annotated[Optional[str],Field(default=None,max_length=50,title="id of the patient",example="P001")]
    name:Annotated[Optional[str],Field(default=None,max_length=50,title="name of the patient",description="name of the patient should be less than 50 characters")]
    city:Annotated[Optional[str],Field(default=None,title="city name of the patient",description="name of the patient should be less than 50 characters")]
    age:Annotated[int,Field(default=None,gt=0,lt=120,title="age of the patient",description="age of the patient should be 0 to 120")]
    gender:Annotated[Literal['male','female','others'],Field(default=None,title="gender of the patient",description="height of the patient should be Male or Female")]
    weight:Annotated[float,Field(default=None,gt=0,title="weight of the patient",description="weight of the patient should be greater than 0")]
    height:Annotated[float,Field(default=None,gt=0,title="height of the patient",description="height of the patient should be greater than 0")]
    
class Patient3(BaseModel):
    id:Annotated[str,Field(...,max_length=50,title="id of the patient",example="P001")]
    city:Annotated[str,Field(...,title="city name of the patient",description="name of the patient should be less than 50 characters")]
    

class Student(BaseModel):
    cgpa:Annotated[float,Field(...,title="cgpa of the student",example="7.5")]
    iq:Annotated[int,Field(...,title="iq of the student",)]




# Function to load data from ".json" file
def load_data():
    with open('patients.json','r') as f: 
        data = json.load(f)
    return data

# Function to save data in json file
def save_data(data):
    with open('patients.json','w+') as f:
        json.dump(data,f)

# Function to load ml model
def load_model():
    with open('model.pkl','rb+') as f : 
        model = pickle.load(f)
    return model

# Function to load scaler (StandardScaler)
def load_scaler():
    with open('scaler.pkl','rb+') as f : 
        scaler = pickle.load(f)
    return scaler



# create routes for the get request
@app.get('/')
def hello():
    return {"message":"Patient Management System API"}


@app.get('/about')
def about():
    return {'message':"This is fully functional api to manage your patient records."}

@app.get('/view')
def view():
    data = load_data()
    return data


@app.get('/view/{id}')
def get_patient_by_id(id:str=Path(...,description="Enter the ID of the patient present in db",example="P001")):
    # ... represents the path parameter is required.
    # Here we can add validation also. 

    data = load_data()

    if id in data : 
        return data[id]
    else:
        # return {'error':"Patient Not Found"}
        raise HTTPException(status_code=404,detail="Patient not found")
    

    # other way 
    # patient = dict(data)
    # return patient.get(id)


@app.get('/patient/view')
def sorted_patients(sortby:str=Query(...,description="sort data on the basis of patient height, weight and bmi",example="?sort_by=bmi"),order=Query(description="ascending or descending",example="order=desc")):

    data = load_data()

    valid_fields = ['height',"weight","bmi"]
    if sortby not in valid_fields : 
        return HTTPException(400,detail=f"Invaild sortby please select from {valid_fields}")
    if order not in ['asc','desc'] : 
        return HTTPException(400,detail=f"Invaild order please select from asc or desc")

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(),key=lambda  x : x.get(sortby,0), reverse=sort_order)
    return sorted_data


@app.post('/create-patient')
def create_patient(patient:Patient):
    data = load_data()
    if patient: 
        if patient.id in data:
            raise HTTPException(status_code=400,detail="Patient already existed")
        else:
            data[patient.id] = patient.model_dump(exclude=['id'])
            save_data(data)
            return JSONResponse(status_code=201,content={"message":"Successfully Created patient"}) 

@app.put('/update-patient/{patient_id}')
def update_patient(patient_id:str,patient:Patient2):
    data = load_data()
    if patient : 
        if patient_id not in data:
            raise HTTPException(status_code=404,detail="Patient not found")
        else:
            existing_patient = data[patient_id]
            updated_patient = patient.model_dump(exclude_unset=True)
            for key, value in updated_patient.items():
                existing_patient[key]= value

            existing_patient['id'] = patient_id
            
            existing_patient_pydantic = Patient(**existing_patient)
            existing_patient=existing_patient_pydantic.model_dump(exclude=['id'])
            # print(existing_patient)
            data[patient_id] = existing_patient
            
            save_data(data)
            return JSONResponse(status_code=200,content={"message":"patient updated successfully"})


@app.patch('/update-patient/update-city')
def update_patient_contact_details(patient:Patient3):
    data = load_data()
    if patient : 
        if patient.id not in data:
            raise HTTPException(status_code=404,detail="Patient not found")
        else:
            data[patient.id]['city'] = patient.model_dump(include=['city'])['city']
            save_data(data)
            return JSONResponse(status_code=200,content={"message":"patient updated successfully"})



@app.delete('/delete-patient/{id}')
def delete_patient(id:str=Path(...,description="Enter the ID of the patient present in db",example="P001")):
    data = load_data()
    if id : 
        if id not in data:
            raise HTTPException(status_code=404,detail="Patient not found")
        else:
            data.pop(id)
            save_data(data)
            return JSONResponse(status_code=200,content={"message":"patient deleted successfully"})
        

@app.post('/predict-placement')
def predict_placement(data:Student):
    model = load_model() 
    x_new = pd.DataFrame(dict(data),index=[0])
    scaler = load_scaler()
    x_new_scaled = scaler.transform(x_new)
    predict = model.predict(x_new_scaled)
    if(predict[0]==1):
        return {"placed":"Yes"}
    else:
        return {"placed":"No"}
    

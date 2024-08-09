from fastapi import FastAPI, Request
from pydantic import BaseModel
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS'u Front end uygulamarı ile iletişim kurulabilmesi için eklenmiştir
origins = [
    "http://localhost:3000", 
    "http://192.168.56.1:3000" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# HuggingFace'den kendi modelimizi çekiyoruz
tokenizer = BertTokenizer.from_pretrained('caesarCITREA/crocus-bert-medical-department-classification')
model = BertForSequenceClassification.from_pretrained('caesarCITREA/crocus-bert-medical-department-classification')

# Modele Ait Departman İsimleri
departments = [
"Kadın Hastalıkları ve Doğum", 
"Ortopedi ve Travmatoloji" ,
"Dermatoloji",
"Göğüs Hastalıkları ",
"Nöroloji",
"Onkoloji" ,
"Dahiliye (İç Hastalıkları)" ,
"Kardiyoloji",
"Psikiyatri" ,
"Pediatri" ,
"Nefroloji" ,
"Fiziksel Tıp ve Rehabilitasyon" ,
"Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji" ,
"Üroloji" ,
"Kulak Burun Boğaz (KBB)", 
"Göz Hastalıkları"
]

class Description(BaseModel):
    text: str


def predict_department(description):
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_class = torch.argmax(logits, dim=1).item()
    
    return departments[predicted_class]

@app.post("/model")
def get_department(description: Description):
    department = predict_department(description.text)
    return {"department": department}



# Fast API Server'ının başlatımı
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

import torch
from transformers import BertTokenizer, BertForSequenceClassification

# HuggingFace'den kendi modelimizi çekiyoruz
tokenizer = BertTokenizer.from_pretrained('caesarCITREA/crocus-bert-medical-department-classification')
model = BertForSequenceClassification.from_pretrained('caesarCITREA/crocus-bert-medical-department-classification')

# Departman isimlerimizi giriyoruz
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






def predict_department(description):
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_class = torch.argmax(logits, dim=1).item()
    
    return departments[predicted_class]

# Example usage
if __name__ == "__main__":
    description = "Merhabalar, bir süredir göğsümdeki sıkışıklık yüzünden nefes nefese kalıyorum."
    department = predict_department(description)
    print(f"Gidilmesi Gereken Departman: {department}")

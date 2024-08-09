import requests

# FastAPI'ın endpoint'ini tanımlıyoruz
url = "http://127.0.0.1:8000/model"

# Modelin İstek Atılarak Örnek Kullanımı
if __name__ == "__main__":
    description = "Son zamanlarda yürüyüş yaparken dizlerimden daha fazla tıkırdama sesi geliyor."
    response = requests.post(url, json={"text": description})
    
    if response.status_code == 200:
        result = response.json()
        print(f"Hasta şu departmana gitmeli: {result['department']}")
    else:
        print(f"İstek şu kod ile hata verdi {response.status_code}")

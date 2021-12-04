import requests

print("="*10)
print("Insira o DNS name do seu Load Balancer: ")
url = input("DNS: ")

print("Insira G para GET")
print("Insira P para POST")
req = input("Request: ")

if(req == "G" or req == "g"):
    res = requests.get(url)
    print(res.json())

elif(req == "P" or req == "p"):
    title = input("Insira o título: ") 
    year = input("Insira o ano: ")
    mon = input("Insira o mês: ")
    day = input("Insira o dia: ")
    hour = input("Insira a hora: ")
    min = input("Insira o minuto: ")
    desc = input("Insira uma descrição: ")

    data = f"{year}-{mon}-{day}T{hour}:{min}"
    print(f"Tarefa criada com título {title}")
    print(f"Data de conclusão: {data}")
    print(f"Descrição: {desc}")

    send = input("Insira S para enviar ou N para cancelar: ")
    if(send == "S" or send == "s"):
        res = requests.post(url, data={
            "title": title,
            "pub_date": data,
            "description": desc
        })

        print(res.json())

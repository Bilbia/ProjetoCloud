import requests

print("="*10)
print("Insira o DNS name do seu Load Balancer: ")
url = input("DNS: ")

print("="*10)
print("Insira G para GET")
print("Insira P para POST")
req = input("Request: ")

if(req == "G" or req == "g"):
    res = requests.get(url)
    print(res.json())

elif(req == "P" or req == "p"):
    print("="*10)
    title = input("Insira o título: ") 
    year = input("Insira o ano: ")
    mon = input("Insira o mês: ")
    day = input("Insira o dia: ")
    hour = input("Insira a hora: ")
    min = input("Insira o minuto: ")
    desc = input("Insira uma descrição: ")

    date = f"{year}-{mon}-{day}T{hour}:{min}"

    print("="*10)
    print(f"Tarefa criada com título {title}")
    print(f"Data de conclusão: {date}")
    print(f"Descrição: {desc}")

    print("="*10)
    send = input("Insira S para enviar ou N para cancelar: ")
    if(send == "S" or send == "s"):
        res = requests.post(url, data={
            "title": title,
            "pub_date": date,
            "description": desc
        })

        print(res.json())
    else:
        quit()

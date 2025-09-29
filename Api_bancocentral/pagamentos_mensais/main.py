import os
import requests
import pandas as pd

# URL da API para os anos 2023, 2024 e 2025
url = (
    "https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/"
    "MeiosdePagamentosMensalDA(AnoMes=@AnoMes)?@AnoMes='2023%2C2024%2C2025'&"
    "$top=100&$format=json&$select=AnoMes,quantidadePix,valorPix,quantidadeTED,quantidadeBoleto,valorBoleto"
)

# Descobrir o caminho da pasta atual (onde está o main.py)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Pasta "data" dentro de pagamentos-mensais
data_dir = os.path.join(base_dir, "data")

# Criar a pasta "data" caso não exista
os.makedirs(data_dir, exist_ok=True)

# Fazer a requisição na API
response = requests.get(url)
if response.status_code == 200:
    dados = response.json()
    df = pd.json_normalize(dados['value'])
    
    # Caminhos completos para salvar
    csv_path = os.path.join(data_dir, "meios_pagamentos_2023_2025.csv")
    json_path = os.path.join(data_dir, "meios_pagamentos_2023_2025.json")

    # Salvar os dados em CSV e JSON
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    df.to_json(json_path, orient="records", force_ascii=False, indent=4)

    print("✅ Arquivos CSV e JSON gerados com sucesso!")
else:
    print(f"❌ Erro ao acessar a API: {response.status_code}")

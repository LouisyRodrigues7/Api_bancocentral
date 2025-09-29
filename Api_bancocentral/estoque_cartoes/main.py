import os
import pandas as pd
import requests

# Selecionando ano e trimestre
anos = [2023, 2024, 2025]
trimestres = [1, 2, 3, 4]

# Percorre cada ano e trimestre
for ano in anos:
    for trimestre in trimestres:
        trimestre_str = f"{ano}-{trimestre}"
        print(f"Baixando dados do trimestre: {trimestre_str}")

        # Setando a URL
        url = f"https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/Quantidadeetransacoesdecartoes(trimestre=@trimestre)?@trimestre='{trimestre_str}'&$top=10000&$format=json&$select=trimestre,nomeBandeira,nomeFuncao,modalidade,qtdCartoesEmitidos,qtdCartoesAtivos"

        # Requisição
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            print(f"⚠️ Erro ao acessar dados de {trimestre_str} - Status: {response.status_code}")
            continue

        # Converter para JSON
        try:
            dados = response.json()
            df = pd.json_normalize(dados['value'])

            # Garante que a pasta esteja dentro de estoque-cartoes
            os.makedirs("estoque-cartoes/data", exist_ok=True)

            # Define os caminhos
            csv_path = f"estoque-cartoes/data/transacoes_cartoes_{trimestre_str}.csv"
            json_path = f"estoque-cartoes/data/transacoes_cartoes_{trimestre_str}.json"

            # Salva em csv e json
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            df.to_json(json_path, orient='records', force_ascii=False, indent=4)

            print(f"✅ Arquivos salvos: {csv_path} | {json_path}")
        except Exception as e:
            print(f"Erro ao processar dados de {trimestre_str}: {e}")

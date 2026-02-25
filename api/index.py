from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
from datetime import datetime
import calendar

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. PEGAR A DATA ATUAL
        hoje = datetime.now()
        dia_atual = hoje.day
        # Descobrir o último dia do mês atual (ex: 28, 30 ou 31)
        _, ultimo_dia_mes = calendar.monthrange(hoje.year, hoje.month)
        
        # 2. CALCULAR A PROPORÇÃO DO MÊS (ex: 0.5 se for metade do mês)
        proporcao_passada = dia_atual / ultimo_dia_mes

        # 3. SEUS DADOS BASE
        servicos = ['OpenAI', 'SendGrid', 'Google Maps', 'Supabase', 'Stripe']
        limites = [400, 100, 1000, 50, 500]
        
        dados_dinamicos = []
        for i in range(len(servicos)):
            # Gera um valor entre 10% e 120% do limite para criar variação real
            uso_fake = round(random.uniform(limites[i] * 0.1, limites[i] * 1.2), 2)
            # Gera uma variação percentual aleatória para o ícone de tendência (ex: +4.2%)
            variacao_fake = round(random.uniform(-5.0, 15.0), 1)
            
            dados_dinamicos.append({
                'servico': servicos[i],
                'uso_atual': uso_fake,
                'limite_alerta': limites[i],
                'variacao': variacao_fake
            })
        
        df = pd.DataFrame(dados_dinamicos)

        # 4. LÓGICA DE ESTIMATIVA (A "MÁGICA" DO PYTHON)
        # Calculamos quanto o usuário gastará até o fim do mês se mantiver o ritmo
        df['estimativa_final'] = (df['uso_atual'] / proporcao_passada).round(2)
        
        # Calculamos a porcentagem de uso atual
        df['percentual_uso'] = ((df['uso_atual'] / df['limite_alerta']) * 100).round(1)
        
        # Status baseado na projeção: se a estimativa final for maior que o limite, CRÍTICO
        df['status'] = df.apply(
            lambda x: 'CRÍTICO' if x['estimativa_final'] > x['limite_alerta'] else 'OK', 
            axis=1
        )

        # 5. ADICIONAR METADADOS DO PERÍODO
        # Criamos uma lista de dicionários (JSON)
        lista_final = df.to_dict(orient='records')
        
        # Envelopamos tudo em um objeto para o Bubble ter infos do mês
        retorno_final = {
            "mes_referencia": hoje.strftime("%B/%Y"), # Ex: February/2026
            "dia_atual": dia_atual,
            "dias_restantes": ultimo_dia_mes - dia_atual,
            "dados": lista_final
        }

        # 6. RESPOSTA DA API
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(retorno_final).encode('utf-8'))
        return

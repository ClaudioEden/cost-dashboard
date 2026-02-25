from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
from datetime import datetime
import calendar
import random # <--- O QUE FALTOU ESTAVA AQUI!

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. PEGAR A DATA ATUAL
        hoje = datetime.now()
        dia_atual = hoje.day
        _, ultimo_dia_mes = calendar.monthrange(hoje.year, hoje.month)
        proporcao_passada = dia_atual / ultimo_dia_mes

        # 2. DEFINIÇÃO DOS SERVIÇOS E ÍCONES (Logos Reais)
        # Usamos uma estrutura de dicionário para facilitar
        config_servicos = [
            {'nome': 'OpenAI', 'limite': 400, 'slug': 'openai'},
            {'nome': 'SendGrid', 'limite': 100, 'slug': 'sendgrid'},
            {'nome': 'Google Maps', 'limite': 1000, 'slug': 'google-maps'},
            {'nome': 'Supabase', 'limite': 50, 'slug': 'supabase'},
            {'nome': 'Stripe', 'limite': 500, 'slug': 'stripe'}
        ]
        
        dados_dinamicos = []
        for item in config_servicos:
            # Gera variação dinâmica a cada clique
            uso_fake = round(random.uniform(item['limite'] * 0.1, item['limite'] * 1.2), 2)
            variacao_fake = round(random.uniform(-5.0, 15.0), 1)
            
            dados_dinamicos.append({
                'servico': item['nome'],
                'uso_atual': uso_fake,
                'limite_alerta': item['limite'],
                'variacao': variacao_fake,
                # URL de Ícone dinâmica para o Bubble exibir
                'icone_url': f"https://img.logo.dev/{item['slug']}.com?token=pk_test_placeholder" 
            })
        
        df = pd.DataFrame(dados_dinamicos)

        # 3. LÓGICA DE ESTIMATIVA
        df['estimativa_final'] = (df['uso_atual'] / proporcao_passada).round(2)
        df['percentual_uso'] = ((df['uso_atual'] / df['limite_alerta']) * 100).round(1)
        df['status'] = df.apply(
            lambda x: 'CRÍTICO' if x['estimativa_final'] > x['limite_alerta'] else 'OK', 
            axis=1
        )

        # 4. MONTAGEM DO RETORNO
        lista_final = df.to_dict(orient='records')
        retorno_final = {
            "mes_referencia": hoje.strftime("%B/%Y"),
            "dia_atual": dia_atual,
            "dias_restantes": ultimo_dia_mes - dia_atual,
            "dados": lista_final
        }

        # 5. RESPOSTA DA API
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(retorno_final).encode('utf-8'))
        return

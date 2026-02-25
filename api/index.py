from http.server import BaseHTTPRequestHandler
import json
import pandas as pd

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Lógica que criamos
        dados = {
            'servico': ['OpenAI', 'SendGrid', 'Google Maps', 'Supabase', 'Stripe'],
            'uso_atual': [450.50, 89.00, 1200.00, 25.00, 510.00],
            'limite_alerta': [400.00, 100.00, 1000.00, 50.00, 500.00]
        }
        df = pd.DataFrame(dados)
        df['status'] = df.apply(lambda x: 'CRÍTICO' if x['uso_atual'] > x['limite_alerta'] else 'OK', axis=1)
        df['percentual_uso'] = (df['uso_atual'] / df['limite_alerta']) * 100
        
        payload = df.to_json(orient='records')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Importante para o Bubble não dar erro de CORS
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        self.wfile.write(payload.encode('utf-8'))
        return

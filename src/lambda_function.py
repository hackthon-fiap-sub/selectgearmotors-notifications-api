import json
import boto3
import os
from datetime import datetime
import logging

# Configurar o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Cliente do SNS para enviar SMS
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Obter a data atual para incluir na mensagem
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Nome da loja e título do documento
    store_name = "Select Gear Motors"
    transaction_title = "Documento de Transação da Compra"
    
    # Processar as mensagens da fila SQS
    for record in event['Records']:
        if 'body' in record:
            logger.info(f"Record Body: {record['body']}")
        else:
            logger.warning("Record does not contain 'body'")
  
        try:
            # A mensagem SQS pode estar dentro de 'body'
            message = json.loads(record['body'])
        except json.JSONDecodeError as e:
            logger.info(f"Erro ao decodificar JSON: {e}")
            raise
        # A mensagem SQS pode estar dentro de 'body'
        message = json.loads(record['body'])
        phone_number = message['phone_number']
        notification_message = message['message']

        # Criar a mensagem personalizada com os novos detalhes
        full_message = (
            f"{transaction_title}\n"
            f"Loja: {store_name}\n"
            f"Data: {current_date}\n\n"
            f"Detalhes: {notification_message}\n"
        )

        # Enviar a mensagem via SMS
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=full_message
        )
        
        logger.info(f"Mensagem enviada para {phone_number}. Resposta: {response}")

    return {
        'statusCode': 200,
        'body': json.dumps('Notificação enviada com sucesso')
    }

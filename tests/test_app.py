# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import json
from lambda_function import lambda_handler
from moto import mock_sns
import boto3

class TestLambdaFunction(unittest.TestCase):

    @mock_sns
    @patch('lambda_function.sns_client')
    def test_lambda_handler(self, mock_sns_client):
        # Configurar o mock do SNS
        sns = boto3.client('sns', region_name='us-east-1')
        topic_arn = sns.create_topic(Name='test_topic')['TopicArn']

        # Mockar a resposta do SNS
        mock_sns_client.publish.return_value = {
            'MessageId': 'test-message-id'
        }

        # Evento simulado do SQS
        event = {
            'Records': [
                {
                    'body': json.dumps({
                        'phone_number': '+5591999999999',
                        'message': 'Compra realizada com sucesso!'
                    })
                }
            ]
        }

        # Contexto simulado (pode ser None)
        context = {}

        # Chamar a função Lambda com o evento simulado
        response = lambda_handler(event, context)

        # Verificar se a função retornou o status code correto
        self.assertEqual(response['statusCode'], 200)

        # Verificar se o publish foi chamado com os argumentos corretos
        mock_sns_client.publish.assert_called_once_with(
            PhoneNumber='+5591999999999',
            Message=(
                'Documento de Transação da Compra\n'
                'Loja: Select Gear Motors\n'
                'Data: '
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                'Detalhes: Compra realizada com sucesso!\n'
            )
        )

if __name__ == '__main__':
    unittest.main()

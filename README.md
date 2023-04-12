# Chatbot Demonstrativo
Chatbot para demonstração de um assistente virtual utilizando NLP com uma rede neural profunda.
Ao fechar a janela a mensagem é enviada ao e-mail.

## Instalação
```
conda create --name chatbot-tensorflow python=3.6;
conda activate chatbot-tensorflow;
pip install -r requirements.txt;
```

Será necessario também criar um arquivo <b>.env</b> com as seguintes chaves:
- SENDGRID_API_KEY: chave privada da SendGrid, onde será nosso provedor de e-mail.
- NOTIFICATION_EMAIL: e-mail particular para notificações, onde será e-mail para recebimentos das mensagens.

## Treinamento do modelo
Devemos executar o notebook <b>train.ipynb</b> completo para assim gerar os arquivos de palavras chaves, classes e o modelo profundo.

## UI do chat
Basta executar o arquivo <b>bot.py</b>.

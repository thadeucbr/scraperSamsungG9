# Monitor de Preço
Este projeto é um script Python que monitora o preço de um Monitor Gamer Curvo Samsung Odyssey 49 no site da Samsung e envia um alerta por e-mail quando o preço cai abaixo do valor máximo estabelecido.

## Requisitos
- Docker
- Conta de e-mail Gmail (para enviar alertas por e-mail)

## Configuração
1. Clone este repositório para o seu computador.
2. Crie um arquivo chamado `.env` na pasta do projeto com as seguintes variáveis:
```
EMAIL_ADDRESS=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_ou_app_password
```
Substitua seu_email@gmail.com pelo seu endereço de e-mail do Gmail e sua_senha_ou_app_password pela sua senha do Gmail ou uma senha de aplicativo gerada (mais seguro).
3. Construa a imagem do Docker executando o seguinte comando no diretório do projeto:
```
docker build -t monitorar-preco .
```
4. Execute o container do Docker com o seguinte comando:
```
docker run -it --name monitorar-preco-container monitorar-preco
```
O script agora está monitorando o preço do monitor no site da Samsung. Quando o preço cai abaixo do valor máximo estabelecido no script, ele enviará um e-mail para o endereço de e-mail configurado no arquivo .env.

## Dependências
O projeto utiliza as seguintes bibliotecas Python:
- beautifulsoup4==4.10.0
- requests==2.26.0
- selenium==3.141.0
- google-auth==2.3.3
- google-auth-oauthlib==0.4.6
- google-auth-httplib2==0.1.0
- google-api-python-client==2.27.0
- python-dotenv==0.19.1

Essas bibliotecas são instaladas automaticamente no container do Docker durante a construção da imagem.
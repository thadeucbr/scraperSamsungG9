# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libfontconfig1 \
    libxrender1 \
    libdbus-glib-1-2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Instale o Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Instale o ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | sed -E "s/Google Chrome ([0-9]+).*/\1/") \
    && CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") \
    && wget "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/ \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Copie os arquivos necessários para o diretório de trabalho
COPY monitorar_preco.py /app
COPY requirements.txt /app
COPY .env /app

# Instale as dependências do projeto
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Execute o script Python
CMD ["python", "monitorar_preco.py"]

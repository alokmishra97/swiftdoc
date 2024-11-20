FROM python:3.10-slim

# Install dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg2 \
    ca-certificates \
    libx11-dev \
    libx11-xcb1 \
    libxcb1-dev \
    libgdk-pixbuf2.0-0 \
    libgl1-mesa-glx \
    libegl1-mesa \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxss1 \
    libnss3 \
    libasound2 \
    libgbm-dev \
    libu2f-udev \
    fonts-liberation \
    xdg-utils \
    --no-install-recommends

# Install Google Chrome
RUN GOOGLE_CHROME_URL="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    wget -q $GOOGLE_CHROME_URL && \
    dpkg -i google-chrome-stable_current_amd64.deb; \
    apt-get install -f -y && \
    rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN LATEST_CHROMEDRIVER=$(curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$LATEST_CHROMEDRIVER/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set Chrome to run in headless mode
ENV DISPLAY=:99
ENV GOOGLE_CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_DRIVER=/usr/local/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy the Python application
COPY . /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python application
CMD ["python", "HoeWarmIsHetInDelft.py"]

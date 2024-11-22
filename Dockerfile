FROM kivy/buildozer:latest

# Copy your project files
COPY . /app

# Set working directory
WORKDIR /app

# Build the APK
CMD buildozer android debug

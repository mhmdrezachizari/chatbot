# AI Telegram Chatbot 🤖

A sophisticated Telegram bot that integrates with AI language models to provide intelligent conversations and image analysis capabilities. This bot supports both text and image processing, with full Persian language support and comprehensive data logging.

## 🌟 Features

### Core Functionality

- **AI-Powered Conversations**: Integrates with Google Gemini 2.0 Flash and OpenAI models through Liara AI platform
- **Image Analysis**: Advanced image processing using OpenAI's Vision models (o4-mini)
- **Multi-Language Support**: Full Persian language interface with English compatibility
- **User Management**: Automatic user registration and profile tracking
- **Message Logging**: Complete conversation history storage
- **Image Storage**: Base64 encoded image storage in database

### Technical Capabilities

- **Asynchronous Processing**: Built with modern async/await patterns for optimal performance
- **Database Integration**: PostgreSQL database for robust data persistence
- **Error Handling**: Comprehensive error management with user-friendly messages
- **Containerized Deployment**: Docker support for easy deployment
- **Environment Configuration**: Secure credential management using environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Telegram Bot Token (from @BotFather)
- Liara AI API Key

### Installation

1. **Clone the repository**

```bash
git clone <your-repository-url>
cd chatbot
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Environment Setup**
   Create a `.env` file in the project root:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
LIARA_API_KEY=your_liara_api_key
BASE_URL=https://api.liara.run/v1
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=your_database_host
POSTGRES_PORT=5432
```

4. **Database Setup**
   The bot automatically creates necessary tables on startup:

- `users`: User profiles and registration data
- `messages`: Complete message history
- `images`: Base64 encoded image storage

5. **Run the Bot**

```bash
python main.py
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the Docker image
docker build -t telegram-chatbot .

# Run the container
docker run -d --env-file .env telegram-chatbot
```

### Docker Compose (Recommended)

```yaml
version: "3.8"
services:
  chatbot:
    build: .
    env_file: .env
    restart: unless-stopped
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 📋 Usage

### Bot Commands

- `/start` - Initialize bot interaction and register user

### Supported Interactions

- **Text Messages**: Send any text message to get AI-powered responses
- **Image Analysis**: Send images for detailed AI analysis and description
- **Automatic Logging**: All interactions are automatically saved to the database

### Example Conversations

```
User: سلام، چطوری؟
Bot: سلام! من یک هوش مصنوعی هستم و آماده کمک به شما می‌باشم...

User: [Sends an image]
Bot: ⏳ در حال تحلیل تصویر توسط هوش مصنوعی...
Bot: [Detailed image analysis in Persian]
```

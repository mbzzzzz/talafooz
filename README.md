# Talafooz - English to Urdu Translator

A beautiful web-based English to Urdu translator application with tangerine and pitch black theme, powered by Hugging Face.

## 🌐 Live Demo
[Deployed on Vercel](https://talafooz-translator.vercel.app)

## Features
- Real-time English to Urdu translation using Hugging Face API
- Modern responsive UI with tangerine and pitch black theme
- Copy to clipboard functionality
- Character count and input validation
- Mobile-friendly design
- Fast and reliable translation service

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/talafooz-translator.git
cd talafooz-translator
```

2. **Install dependencies**
```bash
pip install -r requirements-web.txt
```

3. **Set up environment variables**
```bash
cp env.example .env
# Edit .env and add your Hugging Face API token
```

4. **Get Hugging Face API Token**
   - Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
   - Create a new token
   - Add it to your `.env` file

5. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` to see the application.

## 🚀 Deployment

### Deploy to Vercel

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy to Vercel**
   - Connect your GitHub repository to Vercel
   - Add environment variable: `HUGGINGFACE_API_TOKEN`
   - Deploy!

### Deploy to Heroku

1. **Install Heroku CLI**
2. **Login and create app**
```bash
heroku login
heroku create your-app-name
```

3. **Set environment variables**
```bash
heroku config:set HUGGINGFACE_API_TOKEN=your_token_here
```

4. **Deploy**
```bash
git push heroku main
```

## 🛠️ Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Translation**: Hugging Face API
- **Deployment**: Vercel/Heroku
- **Styling**: Custom CSS with tangerine and pitch black theme

## 📱 Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Translation**: Instant translation using Hugging Face API
- **Character Counter**: Shows input length (max 1000 characters)
- **Copy Functionality**: One-click copy to clipboard
- **Error Handling**: Graceful error messages
- **Loading States**: Visual feedback during translation

## 🔧 Configuration

### Environment Variables
- `HUGGINGFACE_API_TOKEN`: Your Hugging Face API token

### Model Used
- Model: `abdulwaheed1/english-to-urdu-translation-mbart`
- Provider: Hugging Face Inference API
- Language Pair: English (en_XX) → Urdu (ur_PK)

## 📄 License
MIT License - feel free to use this project for your own purposes!

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

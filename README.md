# DeepSeek Question Generator

Deploy deepseek-r1:1.5b model on Render.com for generating questions from text input.

## 🚀 Quick Deploy on Render

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - deepseek question generator"
git remote add origin <your_github_repo_url>
git push -u origin main
```

### 2. Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +" → "Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Environment**: Docker
   - **Port**: 7860
   - **Plan**: Free
   - **Start Command**: (leave blank - Dockerfile handles it)

### 3. Test Your API

**Health Check:**
```bash
curl https://<your-render-url>/
```

**Generate Questions:**
```bash
curl -X POST https://<your-render-url>/generate \
     -H "Content-Type: application/json" \
     -d '{"text": "Python was created by Guido van Rossum in 1991."}'
```

## 📝 API Endpoints

- `GET /` - Health check
- `POST /generate` - Generate questions from input text

### Request Format:
```json
{
  "text": "Your input text here"
}
```

## ⚠️ Notes

- **Startup time**: ~30-60 seconds (model loading)
- **Free tier limits**: 512MB RAM, sleeps after 15 minutes of inactivity
- **Model size**: ~1.1GB (deepseek-r1:1.5b quantized)

## 🔧 Local Development

```bash
# Build and run locally
docker build -t question-generator .
docker run -p 7860:7860 question-generator
``` 
# 🤖 Ollama Setup Guide for Career Intelligence System

This guide will help you set up Ollama for local AI processing in the Career Intelligence System.

## What is Ollama?

Ollama is a tool that allows you to run large language models locally on your machine. This provides:
- **Privacy**: Your data never leaves your machine
- **Cost-effective**: No API costs for AI processing
- **Offline capability**: Works without internet connection
- **Performance**: Fast local processing

## Installation

### Windows
1. Download Ollama from [https://ollama.ai/download](https://ollama.ai/download)
2. Run the installer
3. Ollama will start automatically as a service

### macOS
```bash
# Using Homebrew
brew install ollama

# Or download from https://ollama.ai/download
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## Recommended Models for Career Intelligence

### 1. Llama 2 (Recommended for most users)
```bash
ollama pull llama2
```
- **Size**: ~3.8GB
- **RAM**: 8GB recommended
- **Performance**: Good balance of speed and quality

### 2. Code Llama (Better for technical analysis)
```bash
ollama pull codellama
```
- **Size**: ~3.8GB
- **RAM**: 8GB recommended
- **Performance**: Excellent for code and technical content

### 3. Mistral (Faster, smaller model)
```bash
ollama pull mistral
```
- **Size**: ~4.1GB
- **RAM**: 8GB recommended
- **Performance**: Fast and efficient

### 4. Llama 2 13B (Higher quality, needs more resources)
```bash
ollama pull llama2:13b
```
- **Size**: ~7.3GB
- **RAM**: 16GB recommended
- **Performance**: Higher quality responses

## Quick Setup

1. **Install Ollama** (see above)

2. **Pull a model**:
   ```bash
   ollama pull llama2
   ```

3. **Verify installation**:
   ```bash
   ollama list
   ```

4. **Test the model**:
   ```bash
   ollama run llama2 "Hello, how are you?"
   ```

5. **Start Ollama service** (if not already running):
   ```bash
   ollama serve
   ```

## Configuration

### Update .env file
The Career Intelligence System is already configured to use Ollama. Update your `.env` file if needed:

```bash
# AI Configuration (Ollama preferred, OpenAI fallback)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2  # or your preferred model
```

### Test Integration
1. Start the Career Intelligence backend
2. Visit: http://localhost:8000/api/v1/system/status
3. Check that Ollama shows as available

## Model Comparison

| Model | Size | RAM Needed | Speed | Quality | Best For |
|-------|------|------------|-------|---------|----------|
| mistral | 4.1GB | 8GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Quick responses |
| llama2 | 3.8GB | 8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | General use |
| codellama | 3.8GB | 8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Technical analysis |
| llama2:13b | 7.3GB | 16GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | High quality |

## Troubleshooting

### Ollama not starting
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama manually
ollama serve
```

### Model not found
```bash
# List available models
ollama list

# Pull the model if missing
ollama pull llama2
```

### Memory issues
- Close other applications
- Use a smaller model (mistral)
- Increase virtual memory/swap

### Performance optimization
```bash
# Use GPU acceleration (if available)
ollama run llama2 --gpu

# Adjust context length for faster responses
ollama run llama2 --ctx-size 2048
```

## Advanced Configuration

### Custom Model Parameters
You can create a custom Modelfile for optimized career guidance:

```bash
# Create Modelfile
cat > Modelfile << EOF
FROM llama2
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
SYSTEM You are a professional career advisor with expertise in technology, data science, and business roles. Provide specific, actionable career guidance.
EOF

# Create custom model
ollama create career-advisor -f Modelfile
```

Then update your `.env`:
```bash
OLLAMA_MODEL=career-advisor
```

### Multiple Models
You can have multiple models and switch between them:

```bash
# Pull multiple models
ollama pull llama2
ollama pull codellama
ollama pull mistral

# The system will use the first available model
```

## System Requirements

### Minimum Requirements
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 10GB free space
- **OS**: Windows 10+, macOS 12+, Linux

### Recommended Requirements
- **CPU**: 8 cores
- **RAM**: 16GB
- **Storage**: 20GB free space (SSD preferred)
- **GPU**: Optional but improves performance

## Integration with Career Intelligence

The Career Intelligence System automatically:

1. **Detects Ollama**: Checks if Ollama is running on startup
2. **Falls back gracefully**: Uses OpenAI if Ollama is unavailable
3. **Provides status**: Check `/api/v1/system/status` for service status
4. **Optimizes prompts**: Uses simplified prompts for local models

## Benefits for Career Intelligence

### Privacy
- Student data never leaves your server
- No external API calls for AI processing
- Full control over data processing

### Cost
- No per-request charges
- One-time setup cost only
- Scales with usage without additional fees

### Performance
- Low latency responses
- No network dependency
- Consistent performance

### Customization
- Train models on specific career data
- Customize responses for your institution
- Fine-tune for specific industries

## Next Steps

1. **Install Ollama** following the instructions above
2. **Pull a recommended model** (start with `llama2`)
3. **Test the integration** using the system status endpoint
4. **Monitor performance** and adjust model choice as needed
5. **Consider custom training** for specialized career guidance

## Support

- **Ollama Documentation**: https://ollama.ai/docs
- **Model Library**: https://ollama.ai/library
- **Community**: https://github.com/jmorganca/ollama

---

**🚀 Ready to use local AI for career intelligence!**

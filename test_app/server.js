const express = require('express');
const mongoose = require('mongoose');
const redis = require('redis');
const cors = require('cors');
const helmet = require('helmet');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/testapp', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Redis connection
const redisClient = redis.createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

// Routes
app.get('/', (req, res) => {
  res.json({ 
    message: 'Bedrock Test API',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    database: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
    cache: redisClient.isReady ? 'connected' : 'disconnected'
  });
});

app.get('/api/users', async (req, res) => {
  try {
    // Simulate database query
    const users = [
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
    ];
    
    // Cache result in Redis
    await redisClient.setEx('users', 300, JSON.stringify(users));
    
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
});
// Trigger Bedrock test

// 🤖 Real Amazon Bedrock Test - Tue Sep 23 11:07:03 KST 2025
// This should trigger Claude AI analysis!
console.log('Testing real Amazon Bedrock integration');
// Simple Bedrock test trigger - Tue Sep 23 11:08:02 KST 2025
// OIDC fix test - Tue Sep 23 11:11:13 KST 2025
// Direct Bedrock test - Tue Sep 23 11:12:14 KST 2025

// 🤖 REAL AMAZON BEDROCK TEST - Tue Sep 23 11:15:31 KST 2025
// AWS credentials are now set in GitHub Secrets!
// This should call actual Claude AI for code analysis
console.log('Testing real Amazon Bedrock with credentials!');

// 🎉 CLAUDE MODELS ACTIVATED! - Tue Sep 23 11:19:19 KST 2025
// Claude 3 Haiku ✅
// Claude 3.5 Sonnet ✅  
// Ready for real Amazon AI analysis!
console.log('Claude models are now active - testing real Bedrock!');
// Testing multiple Claude models - Tue Sep 23 11:20:29 KST 2025

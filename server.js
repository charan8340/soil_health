const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path'); // Import path module

const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files (e.g., your HTML file)
app.use(express.static(path.join(__dirname, 'public')));

// Enable CORS
app.use(cors());

// Parse JSON bodies
app.use(bodyParser.json());

app.use(express.json()); // Middleware to parse JSON bodies

app.post('/predict', (req, res) => {
    console.log("Received request body:", req.body);

    const { cropName, soilType, humidity, moisture } = req.body;

    // Validate inputs
    if (typeof cropName !== 'string' || typeof soilType !== 'string' || isNaN(humidity) || isNaN(moisture)) {
        return res.status(400).json({ error: "Invalid input values." });
    }

    // Run the Python script with input parameters
    const python = spawn('python3', ['sample.py', cropName, soilType, humidity, moisture]);

    let result = '';

    python.stdout.on('data', (data) => {
        result += data.toString();
    });

    python.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });

    python.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).json({ error: "Python script failed." });
        }
        res.json({ fertilizer: result.trim() });
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});


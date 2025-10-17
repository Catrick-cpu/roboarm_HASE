const express = require('express');
const app = express();
import {port} from './constants.js'; // Updated port with import from costants for easy switching of port

app.use(express.json());

// Middleware to log the referrer
app.use((req, res, next) => {
    const referrer = req.headers.referer || 'No referrer';
    console.log(`Request received from referrer: ${referrer}`);
    next();
});

// Endpoint to power off the RoboArm
app.get('/api/poweroff', (req, res) => {
    console.log('Powering off the RoboArm...');
    res.json({ message: 'RoboArm is powering off.' });
});

// Endpoint to reboot the RoboArm
app.get('/api/reboot', (req, res) => {
    console.log('Rebooting the RoboArm...');
    res.json({ message: 'RoboArm is rebooting.' });
});

// Endpoint to control motors
app.post('/api/motors/:id', (req, res) => {
    const motorId = parseInt(req.params.id);
    const { steps, clockwise } = req.body;

    // Validate motor ID
    if (motorId < 1 || motorId > 4) {
        return res.status(400).json({ error: 'Invalid motor ID. Must be between 1 and 4.' });
    }

    // Validate steps
    if (typeof steps !== 'number' || steps <= 0) {
        return res.status(400).json({ error: 'Invalid steps. Must be a positive integer.' });
    }

    // Validate clockwise
    if (typeof clockwise !== 'boolean') {
        return res.status(400).json({ error: 'Invalid clockwise value. Must be a boolean.' });
    }

    console.log(`Motor ${motorId} is rotating ${clockwise ? 'clockwise' : 'counterclockwise'} by ${steps} steps.`);
    res.json({
        message: `Motor ${motorId} is rotating ${clockwise ? 'clockwise' : 'counterclockwise'} by ${steps} steps.`,
    });
});

// Endpoint to fetch data (placeholder for IRGENDWAS O_O)
app.get('/api/data/IRGENDWAS', (req, res) => {
    res.json({ data: 'Placeholder data for IRGENDWAS O_O' });
});

// Start the server
app.listen(port, () => {
    console.log(`RoboArm API is running at http://localhost:${port}`);
});
const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');

router.get('/generate-pdf', async (req, res) => {
    try {
        const { dis } = req.query;

        // Check if the offense is cognizable
        // You may need to implement logic to determine cognizability
        const isCognizable = checkCognizable(dis);
 
        if (isCognizable) {
            // Execute the Python script
            const pythonProcess = spawn('python', ['./python_scripts/fir_generator.py', dis]);

            pythonProcess.stdout.on('data', (data) => {
                console.log(`Python script output: ${data}`);
            });

            pythonProcess.stderr.on('data', (data) => {
                console.error(`Error in Python script: ${data}`);
            });

            pythonProcess.on('close', (code) => {
                console.log(`Python script exited with code ${code}`);

                // Notify the client that the PDF has been generated
                res.json({ success: true, message: 'PDF generated successfully' });
            });
        } else {
            res.status(400).json({ success: false, message: 'Offense is not cognizable' });
        }
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ success: false, message: 'Internal server error' });
    }
});

// Function to check cognizability - Replace this with your logic
function checkCognizable(dis) {
    // Implement your logic to check if the offense is cognizable
    // Example: return dis.toLowerCase() === 'cognizable';
    return true; // Modify this based on your criteria
}

module.exports = router; 

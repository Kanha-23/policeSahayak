const express = require("express");
const router = express.Router();
const { exec } = require("child_process");
const path = require("path");

console.log("Current Directory (__dirname):", __dirname);


router.get("/", (req, res) => {
    const complaintId = req.query.complaintId;
    res.render("option", { complaintId });
});
// ... rest of your routes

router.get("/get-offense-type", (req, res) => {
    const complaintId = req.query.complaintId;

    if (!complaintId) {
        return res.status(400).json({ error: "Missing complaintId" });
    }

    const scriptPath = path.join(__dirname, "..", "..", "python_scripts", "fir_generator.py");

    exec(`python "${scriptPath}" "${complaintId}" --check-only`, (error, stdout, stderr) => {
        if (error) {
            console.error("Execution Error:", stderr || error.message);
            return res.status(500).json({ error: "Error in analysis" });
        }
    
        const response = stdout.trim();
        if (!response) {
            return res.status(500).json({ error: "Empty response from script" });
        }
    
        // Split response into type and similarity score (assuming Python script prints both)
        const [offenseType, similarityScore] = response.split("|").map(item => item.trim());
    
        res.json({ type: offenseType, score: similarityScore });
    });
    
    
});

// Route to generate FIR
router.get("/generate-fir", (req, res) => {
    const complaintId = req.query.complaintId;

    if (!complaintId) {
        return res.status(400).json({ error: "Missing complaintId" });
    }

    const scriptPath = path.join(__dirname, "..", "..", "python_scripts", "fir_generator.py");

    exec(`python "${scriptPath}" "${complaintId}"`, (error, stdout, stderr) => {
        if (error) {
            console.error("Execution Error:", stderr || error.message);
            return res.status(500).json({ error: "Error generating FIR" });
        }

        console.log("FIR Generation Output:", stdout);
        res.redirect("/public/pdfs/FIR_Report.pdf");
    });
});

// Route to generate Warrant
router.get("/generate-warrant", (req, res) => {
    const complaintId = req.query.complaintId;

    if (!complaintId) {
        return res.status(400).json({ error: "Missing complaintId" });
    }

    const scriptPath = path.join(__dirname, "..", "..", "python_scripts", "fir_generator.py");

    exec(`python "${scriptPath}" "${complaintId}" --warrant`, (error, stdout, stderr) => {
        if (error) {
            console.error("Execution Error:", stderr || error.message);
            return res.status(500).json({ error: "Error generating Warrant" });
        }

        console.log("Warrant Generation Output:", stdout);
        res.redirect("/public/pdfs/Warrant_Report.pdf");
    });
});

module.exports = router;
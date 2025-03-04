const express = require("express");
const router = express.Router();
const { runPythonScriptAsync } = require("../app");
const path = require('path');

router.get("/webpage", async (req, res) => {
  try {
    // Perform any data processing or fetching required for your webpage
    
    // Get the path to the uploaded image
    const imagePath = path.join(__dirname, "..", "public", "uploads", req.file.filename);

    // Run the Python script with the dynamic image path
    const extractedText = await runPythonScriptAsync('python_scripts/merge.py', imagePath);
    // console.log(extractedText)
    // Render the HBS page and pass the extracted text as a variable
    res.render("webpage", { extractedText });
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
});

module.exports = router;

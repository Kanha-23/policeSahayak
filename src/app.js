const express = require("express");
const hbs = require("hbs");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const session = require("express-session");
const flash = require("connect-flash");
const passport = require("passport");
const LocalStrategy = require("passport-local").Strategy;
const { spawn } = require('child_process');
const pdfRoute = require('./routes/pdf');
const mainRoute = require("./routes/main");
const User = require("./models/users"); 
const userRoute = require("./routes/user");
const authMiddleware = require("./controller/authMiddleware");
const dashboardRoute = require("./routes/dashboard");
const complainformRoute = require("./routes/complainform");
const historyRoute = require("./routes/history");
const generatePDFRoute = require('./routes/generatePDF');
const cors = require('cors');
const { PythonShell } = require('python-shell');
const app = express();
const path = require('path');
const webpageRoute = require("./routes/webpageRoute");const multer = require('multer');
const upload = multer({ dest: 'public/uploads/' });
const optionRoute = require("./routes/option");
const fs = require("fs");





// Add this function to run Python scripts asynchronously
function runPythonScriptAsync(scriptPath, ...args) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', [scriptPath, ...args]);

    let output = [];
    let errorOutput = []; 

    pythonProcess.stdout.on('data', (data) => {
      output.push(data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput.push(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        resolve(output.join(''));
      } else {
        reject(new Error(errorOutput.join('')));
      }
    });
  });
}

  

app.use(bodyParser.urlencoded({ extended: true }));
app.use("/public", express.static("public"));
app.use(upload.single('fileToOCR'));
app.use(cors());
app.use(flash()); 
app.use("/option", optionRoute);

app.use(
  session({
    secret: "your-secret-key", // Change this to a strong, random string
    resave: false,
    saveUninitialized: false,
  })
);

app.use(passport.initialize());
app.use(passport.session());
app.use('', pdfRoute);
passport.use(User.createStrategy());
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

app.set("view engine", "hbs");
app.set("views", "views");
hbs.registerPartials("views/partials");
hbs.registerHelper("eq", function (v1, v2) {
  return v1 === v2;
});

// Your existing routes
app.use("", dashboardRoute);
app.use("", mainRoute);
app.use("", userRoute); 
app.use("", complainformRoute);  
app.use("", historyRoute);   
app.use('/generate-pdf', generatePDFRoute);
app.use("", webpageRoute);             

app.post("/performOCR", async (req, res) => {
  try {
      if (!req.file) {
          return res.status(400).send("No file uploaded.");
      }

      const image_path = path.join(__dirname, "..", "public", "uploads", req.file.filename);
      const pythonProcess = spawn("python", ["python_scripts/merge.py", image_path]);
 
      let output = "";
      pythonProcess.stdout.on("data", (data) => {
          output += data.toString(); 
      });
  
      pythonProcess.stderr.on("data", (data) => {
          console.error("Error:", data.toString());
      });

      pythonProcess.on("close", (code) => {
          if (code === 0) {
              try {
                  const extractedData = JSON.parse(output);
                  console.log("Extracted OCR Data:", extractedData);
                  res.render("webpage", { extractedTextLines: extractedData });
              } catch (error) {
                  console.error("JSON Parsing Error:", error);
                  res.status(500).send("Error processing extracted data.");
              }
          } else {
              res.status(500).send("Python script execution failed.");
          }    
      });
  } catch (error) {
      console.error(error);
      res.status(500).send("Internal Server Error");
  }
});

app.get("/get-ipc-details", (req, res) => {
  const ipcSection = req.query.section;

  if (!ipcSection) {
      return res.status(400).json({ error: "IPC Section is required" });
  }

  const filePath = path.join(__dirname, "..", "csvjson.json");

  fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
          console.error(" Error reading JSON file:", err);
          return res.status(500).json({ error: "Error reading data file" });
      }

      try {
          const ipcData = JSON.parse(data);
          const foundIPC = ipcData.find(item => item["IPC-Section"] == ipcSection);

          if (!foundIPC) {
              console.warn(`⚠ IPC Section ${ipcSection} not found.`);
              return res.status(404).json({ error: "IPC Section not found" });
          }

          res.json({
              section: foundIPC["IPC-Section"],
              type: "Added Manually",
              description: foundIPC.Description
          });
      } catch (jsonError) {
          console.error("❌ JSON Parsing Error:", jsonError);
          return res.status(500).json({ error: "Invalid JSON format in file" });
      }
  });
});



main().catch((err) => console.log(err));

async function main() {
  await mongoose.connect("mongodb://127.0.0.1:27017/RJPOLICE_HACK");
  console.log("Database connected");
}

app.listen(8100, () => {
  console.log("Server started on port 8100");
});
 
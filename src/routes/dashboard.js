const express = require('express');
const router = express.Router();
const connectEnsureLogin = require('connect-ensure-login');
const { PythonShell } = require('python-shell');
const multer = require('multer');

router.get('/dashboard', connectEnsureLogin.ensureLoggedIn(), (req, res) => {
  // This route is protected; only authenticated users can access it
  res.render('dashboard'); // Render your dashboard template or perform other actions
});

module.exports = router;      
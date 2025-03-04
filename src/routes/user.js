const express = require('express');
const router = express.Router();
const passport = require('passport');
const User = require('../models/users');
// const otpController = require("../controller/otpController")

router.get("/signup", (req, res) => {
    res.render("signup")
})

// Signup Route
router.post('/signup', (req, res, next) => {
    // Handle user registration logic here
    const newUser = new User({
        username: req.body.email,
        firstName: req.body.firstName,
        lastName: req.body.lastName,
        country: req.body.country,
        phoneNumber: req.body.phoneNumber
        // Add other user data
    });



    User.register(newUser, req.body.password, (err) => {
        if (err) {
            // Handle registration error
            return next(err);
        }
        // Registration successful, redirect to OTP verification page
        res.redirect(`/login`);
    });
});


router.get("/login", (req, res) => {

    res.render("login")
})
// Login Route
router.post(
    '/login',
    passport.authenticate('local', {
        failureRedirect: '/login',
        successRedirect: '/dashboard',
    }),
    (req, res) => {
        console.log(req.user);
    }
);

router.get('/logout', (req, res) => {
    req.logout(() => {
        res.redirect('/login');
    }); // Passport.js logout
    // Redirect to the login page or any other page you prefer
});

module.exports = router;
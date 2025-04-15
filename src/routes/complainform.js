const express = require('express');
const router = express.Router();
const Complain = require('../models/complain');

// Complaint Form Route
router.get("/complainform", (req, res) => {
    res.render("complainform"); 
});
 
// File Complaint Route  
router.post('/complainform', async (req, res, next) => {
    console.log(req.body);
   
        // Handle filing complaint logic here
        const newComplainForm = new Complain({
            name: req.body.name,
            number: req.body.number,
            email: req.body.email,
            date: req.body.date,
            address: req.body.address,
            occupation: req.body.occupation,
            age: req.body.age,
            loc: req.body.loc, 
            pin: req.body.pin,
            city: req.body.city,
            district: req.body.district,
            state: req.body.state,
            dis: req.body.dis,
            detail: req.body.detail,
            people: req.body.people,
            identityProof: req.body.identityProof,
            proof: req.body.proof,

            aname: req.body.aname,
            aage: req.body.aage,
            aaddress: req.body.aaddress,
            aoccupation: req.body.aoccupation,
            acity: req.body.acity,
            adistrict: req.body.adistrict, 
            astate: req.body.astate




        });
        await newComplainForm.save();
        res.redirect("/dashboard"); 
  
});
module.exports = router; 

  
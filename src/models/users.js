const mongoose = require("mongoose");
const passportLocalMongoose = require('passport-local-mongoose');

const users = mongoose.Schema({ 
    firstName: String, 
    lastName: String,
    phoneNumber: String,  
    country: String,
    email: String, 
    password:String
});  

users.plugin(passportLocalMongoose)

module.exports = mongoose.model("users", users);      
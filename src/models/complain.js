const mongoose = require('mongoose');

const complainFormSchema = new mongoose.Schema({
  name: {
    type: String, 
    // required: true
  }, 
  number: {
    type: String,
    // required: true
  },
  email: {
    type: String,
    // required: true
  },
  date: {
    type: Date,
    // required: true
  },
  loc: {
    type: String,
    // required: true
  },
  pin: {
    type: String, 
    // required: true
  },
  city: {
    type: String, 
    // required: true
  },
  state: {
    type: String,
    // required: true
  },
  district: {
    type: String,
    // required: true
  },
  dis: {
    type: String,
    // required: true
  },
  people: {
    type: Number,
    // required: true
  },
  identityProof: {
    type: String,
    enum: ['aadhar', 'pan', 'voterID'],
    // required: true
  },
  proof: {
    type: String,
  },
  // Additional Fields
  occupation: {
    type: String,
  },
  age: {
    type: Number,
  },
  detail: {  
    type: String,
  },
  aname: {
    type: String,
  },
  aage: {
    type: Number,
  },
  aaddress: {
    type: String,
  },
  aoccupation: {
    type: String,
  },
  acity: {
    type: String,
  },
  adistrict: {
    type: String,
  },
  astate: {
    type: String,
  }
});

const Complain = mongoose.model("Complain", complainFormSchema);

module.exports = Complain;
 
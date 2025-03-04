const express = require("express");
const hbs = require("hbs")
const routes = express.Router();

routes.get("/", (req, res) => {
    res.render("main")
})

module.exports = routes;
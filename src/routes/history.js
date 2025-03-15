const express = require("express");
const routes = express.Router();
const { parse, format } = require('date-fns');
const Complain = require("../models/complain");

// Display all records or filtered records based on search
routes.get("/history", async (req, res) => {
    try {    
        const data = await Complain.find({});
        res.render("history", { Complain: data });
    } catch (error) {
        console.error("Error fetching all data:", error);
        res.status(500).send("An error occurred while fetching all data.");
    } 
});


 
// Handle search requests
routes.post("/history/search", async (req, res) => {
    try {
        let query = {};

        // Fetch all records initially
        const allData = await Complain.find({});

        // Check if a search term is provided
        if (req.body.searchTerm && req.body.searchType !== 'all') {
            const searchTerm = req.body.searchTerm.trim(); 
            // Use a case-insensitive regular expression for searching
            const regex = new RegExp(searchTerm, 'i');

            // Check the search type
            if (req.body.searchType === 'name') {
                // Filter the data based on the 'name' field
                query = { name: regex };
            } else if (req.body.searchType === 'date') {
                // Parse the search date using date-fns
                const parsedDate = parse(searchTerm, 'd-MMM-yyyy', new Date());
                // Format the parsed date as an ISO string
                const searchDate = format(parsedDate, 'yyyy-MM-dd');
                // Filter the data based on the 'date' field
                query = { date: searchDate };
            } else if (req.body.searchType === 'city') {
                // Filter the data based on the 'city' field
                query = { city: regex };
            }
        }

        // Fetch records based on the query
        const filteredData = await Complain.find(query);

        // Combine the results for rendering
        const data = req.body.searchTerm ? filteredData : allData;

        res.render("history", { Complain: data });
    } catch (error) {
        console.error("Error fetching data:", error);
        res.status(500).send("An error occurred while fetching data.");
    }
});

   
module.exports = routes;





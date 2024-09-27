const express = require("express");
const session = require("express-session");
const app = express();
const bcrypt = require("bcrypt");
require("dotenv").config();
const flag = process.env.FLAG;

function filterInput(input) {
  const blacklist = ["<script>", "</script>", "<iframe>, </iframe>"];
  let sanitizedInput = input;

  blacklist.forEach((item) => {
    sanitizedInput = sanitizedInput.replace(new RegExp(item, "gi"), "");
  });

  return sanitizedInput;
}

app.get("/request-flag", async (req, res) => {
  try {
    let message = req.query.message;
    message = filterInput(message);
    return res.render("data", { message });
  } catch (error) {
    console.log(error);
    res.status(500).json({
      status: "Error",
      message: "An error occurred",
    });
  }
});

module.exports = app;

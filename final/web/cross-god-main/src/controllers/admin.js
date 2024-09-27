const express = require("express");
const session = require("express-session");
const path = require("path");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const admin = require("../database/auth");
const bcrypt = require("bcrypt");
const app = express();
const publicDirectoryPath = path.join(__dirname, "../../public");
const viewsPath = path.join(__dirname, "../template");

app.set("view engine", "ejs");
app.set("views", viewsPath);
app.use(express.static(publicDirectoryPath));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

async function createAdminUser() {
  try {
    const username = process.env.USER;
    const password = process.env.PASSWORD;

    const existingUser = await admin.findOne({ username });

    if (existingUser) {
      console.log("Admin account already exists");
      const passwordMatch = await bcrypt.compare(
        password,
        existingUser.password
      );

      if (!passwordMatch) {
        const hashedPassword = await bcrypt.hash(password, 10);
        await admin.findOneAndUpdate(
          { username },
          { password: hashedPassword }
        );
        console.log(`Password for user ${username} updated.`);
      }
    } else {
      const hashedPassword = await bcrypt.hash(password, 10);

      await admin.create({
        username: username,
        password: hashedPassword,
      });
      console.log(`User ${username} created in the database.`);
    }
  } catch (error) {
    console.error("Error creating or Updating admin account: " + error);
  }
}

createAdminUser();

app.post("/admin/login", async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await admin.findOne({ username });

    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    const passwordMatch = await bcrypt.compare(password, user.password);

    if (!passwordMatch) {
      return res.status(401).json({ error: "Invalid password" });
    }

    req.session.user = user;

    res.redirect("/admin/dashboard");
  } catch (error) {
    res
      .status(502)
      .json({ error: "Error login to the admin account: " + error });
  }
});

app.get("/admin/login", async (req, res) => {
  try {
    res.render("login");
  } catch (error) {
    console.log("Error opening login page: " + error);
    res.status(502).json({ error: "Error: " + error });
  }
});

app.post("/admin/logout", async (req, res) => {
  try {
    req.session.destroy();
    res.redirect("/admin/login");
  } catch (error) {
    console.log("Error logging out: " + error);
    res.status(502).json({ error: "Error: " + error });
  }
});

module.exports = app;

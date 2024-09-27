require("dotenv").config();
const express = require("express");
const session = require("express-session");
const bcrypt = require("bcrypt");
const https = require("https");
const path = require("path");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const mongoSanitize = require("express-mongo-sanitize");
const generateRandomKey = require("./middlware/generateRandomKey");
const getRecaptcha = require("./middlware/recaptcha");
const Keys = require("../database/key");
const generatedKeys = require("../database/generatedKeys");

const publicDirectoryPath = path.join(__dirname, "../../public");
const viewsPath = path.join(__dirname, "../template");

const app = express();
const checkpointAmount = process.env.CHECKPOINT || 3;

app.set("view engine", "ejs");
app.set("views", viewsPath);
app.use(express.static(publicDirectoryPath));
app.use(express.json());
app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(mongoSanitize());

app.get("/api/getkey/proceed-hwid", async (req, res) => {
  try {
    const { hwid } = req.query;
    if (!hwid) {
      return res.status(400).json({ error: "HWID Required!" });
    }

    res.cookie("hwid", hwid, { maxAge: 3600000, httpOnly: true });
    req.session.hwid = hwid;

    return res.redirect("/api/getkey");
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "An error occurred" });
  }
});

app.get("/api/getkey", async (req, res) => {
  try {
    const hwid = req.cookies.hwid;
    const keyActive = await Keys.findOne({ hwid: hwid });

    if (!hwid) {
      return res.status(400).json({ error: "HWID Required!" });
    }

    if (keyActive) {
      const currentDate = new Date();
      if (keyActive.expiresAt < currentDate) {
        await Keys.findOneAndDelete({ hwid: hwid });
        return res.redirect("/api/getkey");
      }
      return res.render("./getkey/rendered", { keyValue: keyActive.value });
    }

    req.session.hwid = hwid;
    req.session.checkpoints = req.session.checkpoints || {};
    let checkpointCount = req.session.checkpoints[hwid] || 0;

    if (checkpointCount >= checkpointAmount) {
      const expiresAt = new Date(
        Date.now() + (parseInt(process.env.KEYEXPIRATION) || 24) * 3600 * 1000
      );
      const currentDate = new Date();
      const keyValue = `${process.env.SERVICE_NAME}_${generateRandomKey()}`;
      const newKey = new Keys({
        value: keyValue,
        hwid: hwid,
        createdAt: currentDate,
        expiresAt: expiresAt,
        isPremium: false,
      });

      await newKey.save();
      req.session.checkpoints[hwid] = 0;
      return res.render("./getkey/rendered", { keyValue: newKey.value });
    } else {
      return res.render("./getkey/index", {
        checkpointCount: checkpointCount + 1,
        totalCheckpoint: checkpointAmount,
        expiresKey: process.env.KEYEXPIRATION,
        recaptchaSiteKey: process.env.RECAPTCHA_SITE_KEY,
        recaptchaSecretKey: process.env.RECAPTCHA_SECRET_KEY,
      });
    }
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .json({ error: "An error occurred, failed to generate key" });
  }
});

app.post("/api/getkey/proceed", async (req, res) => {
  try {
    const hwid = req.session.hwid;
    const { "g-recaptcha-response": recaptchaResponse } = req.body;

    if (!hwid) {
      return res.status(400).json({ error: "HWID not found in session" });
    }

    const secretKey = process.env.RECAPTCHA_SECRET_KEY;
    const verificationUrl = `https://www.google.com/recaptcha/api/siteverify?secret=${secretKey}&response=${recaptchaResponse}`;

    https.get(verificationUrl, (verificationRes) => {
      let data = "";

      verificationRes.on("data", (chunk) => {
        data += chunk;
      });

      verificationRes.on("end", () => {
        const responseData = JSON.parse(data);

        if (!responseData.success) {
          return res.status(406).json({ error: "Please solve the Recaptcha" });
        }

        req.session.checkpoints = req.session.checkpoints || {};
        let checkpointCount = req.session.checkpoints[hwid] || 0;

        if (checkpointCount >= checkpointAmount) {
          return res.redirect("/api/getkey");
        }

        req.session.checkpoints[hwid] = checkpointCount + 1;
        return res.redirect(process.env.ADSLINK);
      });
    });
  } catch (error) {
    console.error("An error occurred:", error);
    res.status(500).json({ error: "An error occurred" });
  }
});

module.exports = app;

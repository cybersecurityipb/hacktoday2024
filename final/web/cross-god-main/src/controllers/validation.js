const express = require("express");
const session = require("express-session");
const app = express();
const bcrypt = require("bcrypt");
const keys = require("../database/key");
const generatedKeys = require("../database/generatedKeys");
require("dotenv").config();
const flag = process.env.FLAG;
app.get("/api/validate", async (req, res) => {
  try {
    const { key, hwid } = req.query;
    if (!key || !hwid) {
      return res.status(400).json({
        status: "Error",
        message: "All fields are required",
      });
    }

    let validateKey = await keys.findOne({ value: key, hwid: hwid });

    if (!validateKey) {
      const validateGeneratedKey = await generatedKeys.findOne({ value: key });

      if (!validateGeneratedKey) {
        return res.status(404).json({
          status: "Invalid key",
          message: "The provided key is invalid.",
        });
      } else {
        const currentDate = new Date();
        if (validateGeneratedKey.expiresAt < currentDate) {
          await generatedKeys.findOneAndDelete({ value: key });
          return res.status(410).json({
            status: "Invalid key",
            message: "The provided key is expired.",
          });
        }

        await keys.create({
          value: key,
          hwid,
          createdAt: currentDate,
          expiresAt: validateGeneratedKey.expiresAt,
          isPremium: validateGeneratedKey.isPremium,
        });

        await generatedKeys.findOneAndDelete({ value: key });
        if (validateGeneratedKey.isPremium === true) {
          return res.json({
            status: "Valid Key",
            message: flag,
            isPremium: validateGeneratedKey.isPremium,
          });
        }
        return res.json({
          status: "Valid key",
          message: "The provided key is valid and has been activated.",
          isPremium: validateGeneratedKey.isPremium,
        });
      }
    }

    const currentDate = new Date();
    if (validateKey.expiresAt < currentDate) {
      await keys.findOneAndDelete({ value: key, hwid: hwid });
      return res.status(410).json({
        status: "Invalid key",
        message: "The provided key is expired.",
        isPremium: validateKey.isPremium,
      });
    }

    return res.json({
      status: "Valid key",
      message: "The provided key is valid.",
      isPremium: validateKey.isPremium,
    });
  } catch (error) {
    console.log(error);
    res.status(500).json({
      status: "Error",
      message: "An error occurred",
    });
  }
});

module.exports = app;

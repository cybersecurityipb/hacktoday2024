const express = require("express");
const path = require("path");
const session = require("express-session");
const app = express();
const bot = require("./middlware/botSrc");
require("dotenv").config();

app.use(express.urlencoded({ extended: false }));
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

const rateLimit = require("express-rate-limit");

if (process.env.USE_PROXY) {
  app.set("trust proxy", 1);
}

// Use the same encoding logic
const charMap = {
  a: "m",
  b: "n",
  c: "b",
  d: "v",
  e: "c",
  f: "x",
  g: "z",
  h: "a",
  i: "s",
  j: "d",
  k: "f",
  l: "g",
  m: "h",
  n: "j",
  o: "k",
  p: "l",
  q: "p",
  r: "o",
  s: "i",
  t: "u",
  u: "y",
  v: "t",
  w: "r",
  x: "e",
  y: "w",
  z: "q",
  A: "M",
  B: "N",
  C: "B",
  D: "V",
  E: "C",
  F: "X",
  G: "Z",
  H: "A",
  I: "S",
  J: "D",
  K: "F",
  L: "G",
  M: "H",
  N: "J",
  O: "K",
  P: "L",
  Q: "P",
  R: "O",
  S: "I",
  T: "U",
  U: "Y",
  V: "T",
  W: "R",
  X: "E",
  Y: "W",
  Z: "Q",
  0: "5",
  1: "6",
  2: "7",
  3: "8",
  4: "9",
  5: "0",
  6: "1",
  7: "2",
  8: "3",
  9: "4",
  ":": ";",
  ";": ":",
  "@": "!",
};

const reverseCharMap = Object.fromEntries(
  Object.entries(charMap).map(([key, value]) => [value, key])
);

function complexEncode(str) {
  let encoded = "";
  for (let i = 0; i < str.length; i++) {
    let charCode = str.charCodeAt(i);
    charCode += (i % 5) + 1;
    encoded += String.fromCharCode(charCode);
  }
  encoded = encoded
    .split("")
    .map((char) => charMap[char] || char)
    .join("");
  encoded = encoded.split("").reverse().join("");
  return encoded;
}

const creds = process.env.USER + ":" + process.env.PASSWORD;
const encodedCreds = complexEncode(creds);

const limit = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 5,
  handler: (req, res, _next) => {
    const timeRemaining = Math.ceil(
      (req.rateLimit.resetTime - Date.now()) / 1000
    );
    res.status(429).json({
      error: `Too many requests, please try again after ${timeRemaining} seconds.`,
    });
  },
});

app.post("/report", limit, async (req, res) => {
  try {
    const { url } = req.body;

    if (!url) {
      return res.status(400).json({ error: "URL is missing." });
    }

    if (!RegExp(bot.urlRegex).test(url)) {
      return res.status(422).json({
        error: `URL did not match the required regex format: ${bot.urlRegex}`,
      });
    }

    if (await bot.visitUrl(url, encodedCreds)) {
      return res.json({ success: "Admin successfully visited the URL." });
    } else {
      return res.status(500).json({ error: "Admin failed to visit the URL." });
    }
  } catch (error) {
    console.log(error);
    res.status(500).json({
      status: "Error",
      message: "An error occurred",
    });
  }
});

app.get("/report", (_, res) => {
  try {
    res.render("../../../views/report");
  } catch (error) {
    console.log(error);
    res.status(500).json({
      status: "Error",
      message: "An error occurred",
    });
  }
});

module.exports = app;

require("dotenv").config();
const express = require("express");
const session = require("express-session");
const path = require("path");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const layouts = require("express-ejs-layouts");
const flash = require("connect-flash");
const mongoSanitize = require("express-mongo-sanitize");
const cookieParser = require("cookie-parser");
const cors = require("cors");
const app = express();
const port = process.env.PORT || 8080;

const auth = require("../controllers/admin");
const dashboard = require("../controllers/adminDashboard");
const flag = require("../controllers/requestFlag");
const getkey = require("../controllers/getkey");
const validation = require("../controllers/validation");
const report = require("../controllers/bot");
const publicDirectoryPath = path.join(__dirname, "../../public");
const viewsPath = path.join(__dirname, "../template");

app.set("view engine", "ejs");
app.set("views", viewsPath);
app.use(express.static(publicDirectoryPath));

app.use(cookieParser());

mongoose.connect("mongodb://127.0.0.1:27017/cross-god", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(
  session({
    secret: "HASHIHXXXXWEBSSSSASDSDWASD",
    resave: false,
    saveUninitialized: false,
  })
);

app.use(flash());
app.use(mongoSanitize());
app.use(cors());

/*
=====================================================
===== ROUTES =========================================
=====================================================
*/
app.use(auth);
app.use(dashboard);
app.use(getkey);
app.use(validation);
app.use(flag);
app.use(report);
app.get("/", (req, res) => {
  res.render("index");
});

/*
=====================================================
===== ROUTES =========================================
=====================================================
*/

app.listen(port, () => {
  console.log(`Server is up on port ${port}`);
});

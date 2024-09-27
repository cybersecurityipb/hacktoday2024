const express = require("express");
const session = require("express-session");
const path = require("path");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const admin = require("../database/auth");
const keys = require("../database/key");
const generatedKeys = require("../database/generatedKeys");
const bcrypt = require("bcrypt");
const app = express();
const generateRandomKey = require("./middlware/generateRandomKey");
const publicDirectoryPath = path.join(__dirname, "../../public");
const viewsPath = path.join(__dirname, "../template");

app.set("view engine", "ejs");
app.set("views", viewsPath);
app.use(express.static(publicDirectoryPath));

function formatDate(date) {
  return new Date(date).toLocaleDateString();
}

app.get("/admin/manage", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.redirect("/admin/login");
    }

    const currentPage = parseInt(req.query.page) || 1;
    const keysPerPage = 15;
    const skip = (currentPage - 1) * keysPerPage;
    const searchTerm = req.query.search || "";
    const searchRegex = new RegExp(searchTerm, "i");
    const totalPages = Math.ceil((await keys.countDocuments({})) / keysPerPage);

    const currentPageGenerated = parseInt(req.query.pageGenerated) || 1;
    const keysPerPageGenerated = 15;
    const skipGenerated = (currentPageGenerated - 1) * keysPerPageGenerated;
    const searchTermGenerated = req.query.searchGenerated || "";
    const searchRegexGenerated = new RegExp(searchTermGenerated, "i");
    const totalPagesGenerated = Math.ceil(
      (await generatedKeys.countDocuments({})) / keysPerPageGenerated
    );

    const normalKeysRender = await keys
      .find({ isPremium: false, value: searchRegex })
      .skip(skip)
      .limit(keysPerPage);
    const premiumKeysRender = await keys
      .find({ isPremium: true, value: searchRegex })
      .skip(skip)
      .limit(keysPerPage);
    const activeKeysRender = await keys
      .find({ value: searchRegex })
      .skip(skip)
      .limit(keysPerPage);
    const generatedKeysRender = await generatedKeys
      .find({ value: searchRegexGenerated })
      .skip(skipGenerated)
      .limit(keysPerPageGenerated);
    const generatedPremiumKeysRender = await generatedKeys
      .find({ isPremium: true, value: searchRegexGenerated })
      .skip(skipGenerated)
      .limit(keysPerPageGenerated);
    const generatedNormalKeysRender = await generatedKeys
      .find({ isPremium: false, value: searchRegexGenerated })
      .skip(skipGenerated)
      .limit(keysPerPageGenerated);

    res.render("./dashboard/manage", {
      data: {
        normalKeysRender: normalKeysRender,
        premiumKeysRender: premiumKeysRender,
        formatDate: formatDate,
        activeKeysRender: activeKeysRender,
        generatedKeysRender: generatedKeysRender,
        currentPage: currentPage,
        totalPages: totalPages,
        currentPageGenerated: currentPageGenerated,
        totalPagesGenerated: totalPagesGenerated,
        searchTerm: searchTerm,
        searchTermGenerated: searchTermGenerated,
      },
    });
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.get("/admin/dashboard", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.redirect("/admin/login");
    }

    const daysToShow = 7;
    const dates = [];
    const keysCountByDay = [];
    const generatedKeysCountByDay = [];

    for (let i = 0; i < daysToShow; i++) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      dates.unshift(date.toISOString().split("T")[0]);

      const keysCount = await keys.countDocuments({
        createdAt: {
          $gte: new Date(date.setUTCHours(0, 0, 0, 0)),
          $lt: new Date(date.setUTCHours(23, 59, 59, 999)),
        },
      });

      const generatedKeysCount = await generatedKeys.countDocuments({
        createdAt: {
          $gte: new Date(date.setUTCHours(0, 0, 0, 0)),
          $lt: new Date(date.setUTCHours(23, 59, 59, 999)),
        },
      });

      keysCountByDay.unshift(keysCount);
      generatedKeysCountByDay.unshift(generatedKeysCount);
    }

    const normalKeysCount = await keys.countDocuments({ isPremium: false });
    const premiumKeysCount = await keys.countDocuments({ isPremium: true });
    const generatedPremiumKeysCount = await generatedKeys.countDocuments({
      isPremium: true,
    });
    const generatedNormalKeysCount = await generatedKeys.countDocuments({
      isPremium: false,
    });

    res.render("dashboard/index", {
      data: {
        normalKeysCount,
        premiumKeysCount,
        generatedPremiumKeysCount,
        generatedNormalKeysCount,
        dates,
        keysCountByDay,
        generatedKeysCountByDay,
      },
    });
  } catch (error) {
    console.error("Error fetching data: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/generate-key", async (req, res) => {
  try {
    const { expiresAt, isPremium, howMuchKey } = req.body;
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    if (!expiresAt || !isPremium || !howMuchKey) {
      return res.status(401).json({ error: "All fields are required" });
    }

    const generatedKeysArr = [];
    const currentDate = new Date();
    for (let i = 0; i < howMuchKey; i++) {
      const keyValue = process.env.SERVICE_NAME + "_" + generateRandomKey();
      const newKey = await generatedKeys.create({
        value: keyValue,
        createdAt: currentDate,
        expiresAt,
        isPremium,
      });
      generatedKeysArr.push(newKey.value);
    }

    res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/delete-key/:id", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const keyId = req.params.id;
    await keys.findByIdAndDelete(keyId);

    return res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/delete-key-premium", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    await keys.deleteMany({ isPremium: true });
    return res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/delete-key-normal", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    await keys.deleteMany({ isPremium: false });
    return res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/delete-generated-key/:id", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const keyId = req.params.id;
    await generatedKeys.findByIdAndDelete(keyId);

    return res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/delete-generated-key-all", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    await generatedKeys.deleteMany({});
    return res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/reset-hwid/:id", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const keyId = req.params.id;
    const key = await keys.findById(keyId);
    await generatedKeys.create({
      value: key.value,
      expiresAt: key.expiresAt,
      isPremium: key.isPremium,
    });

    await keys.findByIdAndDelete(keyId);

    res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/edit-ispremium-key/:id", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const keyId = req.params.id;
    const key = await keys.findById(keyId);
    await keys.findByIdAndUpdate(keyId, { isPremium: !key.isPremium });

    res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/admin/manage/edit-ispremium-generatedkey/:id", async (req, res) => {
  try {
    if (!req.session.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const keyId = req.params.id;
    const key = await generatedKeys.findById(keyId);
    await generatedKeys.findByIdAndUpdate(keyId, {
      isPremium: !key.isPremium,
    });

    res.redirect("/admin/manage");
  } catch (error) {
    console.error("Error fetching users: " + error);
    res.status(500).json({ error: "Internal server error" });
  }
});

module.exports = app;

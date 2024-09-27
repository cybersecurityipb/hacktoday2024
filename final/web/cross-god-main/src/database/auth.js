const mongoose = require("mongoose");

mongoose
  .connect("mongodb://127.0.0.1:27017/cross-god")
  .then(() => {
    console.log("mongoose connected for key model");
  })
  .catch((e) => {
    console.log("failed to connect to MongoDB");
  });

const authSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
  },
  password: {
    type: String,
    required: true,
  },
});

const auth = mongoose.model("admin", authSchema);
module.exports = auth;

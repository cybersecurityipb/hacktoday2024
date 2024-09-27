const mongoose = require("mongoose");

mongoose
  .connect("mongodb://127.0.0.1:27017/cross-god", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("mongoose connected for key model");
  })
  .catch((e) => {
    console.log("failed to connect to MongoDB", e);
  });

const generatedKeySchema = new mongoose.Schema(
  {
    value: {
      type: String,
      required: true,
    },
    createdAt: {
      type: Date,
      required: true,
    },
    expiresAt: {
      type: Date,
    },
    isPremium: {
      type: Boolean,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

const GeneratedKeys = mongoose.model("GeneratedKeys", generatedKeySchema);
module.exports = GeneratedKeys;

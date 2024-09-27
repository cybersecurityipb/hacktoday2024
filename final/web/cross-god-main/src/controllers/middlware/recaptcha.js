const RecaptchaV2 = require("express-recaptcha").RecaptchaV2;

function getRecaptcha() {
  global.recaptcha =
    global.recaptcha ||
    new RecaptchaV2(
      process.env.RECAPTCHA_SITE_KEY,
      process.env.RECAPTCHA_SECRET_KEY
    );
  const recaptcha = global.recaptcha;
  return recaptcha;
}

module.exports = getRecaptcha;

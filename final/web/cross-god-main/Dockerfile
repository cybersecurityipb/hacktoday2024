FROM node:18-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

ENV PORT=3000 \
    USER=test \
    PASSWORD=test \
    SERVICE_NAME=NINJA \
    RECAPTCHA_SITE_KEY=6Ld0zOIpAAAAAFY1f5Nkfrz06vgZWzn9ix7YWRe3 \
    RECAPTCHA_SECRET_KEY=6Ld0zOIpAAAAAAsrnpYnHME0I5BJnALzTnNurLb7 \
    CHECKPOINT=3 \
    KEYEXPIRATION=24 \
    APPLIMITTIME=60 \
    APPLIMIT=5 \
    APPURL=http://localhost:3000 \
    APPURLREGEX="^https?://.*" \
    ADSLINK=your_ads_link_here \
    REFERER=your_referer_here \
    BROWSER=chromium \
    FLAG=hacktoday{REDACTED}

# Expose the application's port (default is 3000)
EXPOSE 3000

# Start the application
CMD ["npm", "start"]

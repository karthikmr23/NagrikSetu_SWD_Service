const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let c = fs.readFileSync(filePath, "utf8");
c = c.replace(
  "  HeartHandshake,",
  "  HeartHandshake, ExternalLink, Bell, Building, Building2, Download, MessageSquare,"
);
fs.writeFileSync(filePath, c, "utf8");
console.log("Added missing imports");

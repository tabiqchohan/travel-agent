const fs = require('fs');
const path = require('path');

const renderUrl = process.env.RENDER_URL || '';
const indexPath = path.join(__dirname, 'index.html');

let html = fs.readFileSync(indexPath, 'utf-8');
html = html.replace('__RENDER_URL__', renderUrl);
fs.writeFileSync(indexPath, html);

console.log(`✅ Replaced __RENDER_URL__ with: ${renderUrl || '(empty - using fallback)'}`);

const fs = require('fs');
const path = require('path');

const rootDir = path.resolve('scripts');
const violations = [];

function walk(dir) {
   const entries = fs.readdirSync(dir, { withFileTypes: true });

   entries.forEach(entry => {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
         walk(fullPath);
         return;
      }

      if (!entry.isFile() || !entry.name.endsWith('.js')) {
         return;
      }

      if (entry.name.includes('-')) {
         violations.push(path.relative(process.cwd(), fullPath));
      }
   });
}

walk(rootDir);

if (violations.length > 0) {
   console.error('JavaScript filenames must use camelCase or lower-case names without hyphens:');
   violations.forEach(file => {
      console.error(file);
   });
   process.exit(1);
}

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const ROOT = process.cwd();
const CONFIG_PATH = path.join(ROOT, 'tools/lint/jsOneClassPerFile.json');

function loadConfig() {
   if (!fs.existsSync(CONFIG_PATH)) {
      return {
         include: [],
         exclude: [],
      };
   }

   return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function toPosix(filePath) {
   return filePath.split(path.sep).join('/');
}

function globToRegExp(pattern) {
   const escaped = pattern
      .replace(/[.+^${}()|[\]\\]/g, '\\$&')
      .replace(/\*\*/g, '::DOUBLESTAR::')
      .replace(/\*/g, '[^/]*')
      .replace(/::DOUBLESTAR::/g, '.*');

   return new RegExp(`^${escaped}$`);
}

function matchesAny(relativePath, patterns) {
   return patterns.some(pattern => globToRegExp(pattern).test(relativePath));
}

function camelToPascal(stem) {
   return stem.charAt(0).toUpperCase() + stem.slice(1);
}

function walkJsFiles(dir, files = []) {
   const entries = fs.readdirSync(dir, { withFileTypes: true });

   entries.forEach(entry => {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
         walkJsFiles(fullPath, files);
         return;
      }

      if (entry.isFile() && entry.name.endsWith('.js')) {
         files.push(fullPath);
      }
   });

   return files;
}

function topLevelClassNames(source) {
   const names = [];
   const classPattern = /^(?:export\s+(?:default\s+)?)?class\s+([A-Za-z_$][\w$]*)/gm;
   let match = classPattern.exec(source);

   while (match) {
      names.push(match[1]);
      match = classPattern.exec(source);
   }

   return names;
}

function checkFile(fullPath) {
   const relativePath = toPosix(path.relative(ROOT, fullPath));
   const expected = camelToPascal(path.parse(fullPath).name);
   const source = fs.readFileSync(fullPath, 'utf8');
   const classes = topLevelClassNames(source);

   if (classes.length === 0) {
      return `${relativePath}: expected exactly one class named ${expected}, found none`;
   }

   if (classes.length > 1) {
      return `${relativePath}: expected exactly one class, found ${classes.length}: ${classes.join(', ')}`;
   }

   if (classes[0] !== expected) {
      return `${relativePath}: class ${classes[0]} must match file name ${expected}`;
   }

   return null;
}

function main() {
   const config = loadConfig();
   const include = config.include ?? [];
   const exclude = config.exclude ?? [];
   const scriptsDir = path.join(ROOT, 'scripts');
   const violations = [];

   walkJsFiles(scriptsDir).forEach(fullPath => {
      const relativePath = toPosix(path.relative(ROOT, fullPath));

      if (include.length > 0 && !matchesAny(relativePath, include)) {
         return;
      }

      if (matchesAny(relativePath, exclude)) {
         return;
      }

      const violation = checkFile(fullPath);

      if (violation) {
         violations.push(violation);
      }
   });

   if (violations.length === 0) {
      return 0;
   }

   violations.forEach(violation => {
      console.error(violation);
   });
   console.error(`\nFound ${violations.length} one-class-per-file violation(s).`);
   return 1;
}

process.exit(main());

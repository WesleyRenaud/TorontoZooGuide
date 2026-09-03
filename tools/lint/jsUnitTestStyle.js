import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const ROOT = process.cwd();
const CONFIG_PATH = path.join(ROOT, 'tools/lint/jsUnitTestStyle.json');

const FULL_TEST_NAME_RE = /^Test_[A-Z][A-Za-z0-9]*_Test[A-Za-z0-9][A-Za-z0-9]*_Expect[A-Za-z0-9][A-Za-z0-9]*$/;
const SHORT_TEST_NAME_RE = /^Test_[A-Za-z][A-Za-z0-9_]*$/;

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

function walkTestFiles(dir, files = []) {
   if (!fs.existsSync(dir)) {
      return files;
   }

   const entries = fs.readdirSync(dir, { withFileTypes: true });

   entries.forEach(entry => {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
         walkTestFiles(fullPath, files);
         return;
      }

      if (entry.isFile() && entry.name.endsWith('.test.mjs')) {
         files.push(fullPath);
      }
   });

   return files;
}

function lineNumberAtIndex(source, index) {
   let line = 1;

   for (let i = 0; i < index && i < source.length; i += 1) {
      if (source[i] === '\n') {
         line += 1;
      }
   }

   return line;
}

function extractTestTitles(source) {
   const titles = [];
   const pattern = /\b(?:it|test)\s*\(\s*(['"`])([\s\S]*?)\1/g;
   let match = pattern.exec(source);

   while (match) {
      titles.push({
         title: match[2],
         index: match.index,
      });
      match = pattern.exec(source);
   }

   return titles;
}

function isValidTestTitle(title) {
   if (FULL_TEST_NAME_RE.test(title)) {
      return true;
   }

   // Short form for table-driven / single-method coverage, matching Python's
   // parametrized Test_[Method] exemption.
   return SHORT_TEST_NAME_RE.test(title);
}

function checkFile(fullPath) {
   const relativePath = toPosix(path.relative(ROOT, fullPath));
   const source = fs.readFileSync(fullPath, 'utf8');
   const violations = [];

   extractTestTitles(source).forEach(({ title, index }) => {
      if (isValidTestTitle(title)) {
         return;
      }

      const line = lineNumberAtIndex(source, index);
      violations.push(
         `${relativePath}:${line}: "${title}" must match `
         + 'Test_[Method]_Test[Scenario]_Expect[Outcome] '
         + '(table-driven tests may use Test_[Method] only)'
      );
   });

   return violations;
}

function main() {
   const config = loadConfig();
   const include = config.include ?? [];
   const exclude = config.exclude ?? [];
   const testsDir = path.join(ROOT, 'tests/scripts');
   const violations = [];

   walkTestFiles(testsDir).forEach(fullPath => {
      const relativePath = toPosix(path.relative(ROOT, fullPath));

      if (include.length > 0 && !matchesAny(relativePath, include)) {
         return;
      }

      if (matchesAny(relativePath, exclude)) {
         return;
      }

      violations.push(...checkFile(fullPath));
   });

   if (violations.length === 0) {
      return 0;
   }

   violations.forEach(violation => {
      console.error(violation);
   });
   console.error(`\nFound ${violations.length} unit-test style violation(s).`);
   return 1;
}

process.exit(main());

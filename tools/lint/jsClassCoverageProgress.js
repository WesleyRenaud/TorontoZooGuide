import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const ROOT = process.cwd();
const ONE_CLASS_CONFIG = path.join(ROOT, 'tools/lint/jsOneClassPerFile.json');
const UNIT_TEST_CONFIG = path.join(ROOT, 'tools/lint/jsUnitTestStyle.json');

function loadConfig(configPath) {
   if (!fs.existsSync(configPath)) {
      return {
         include: [],
         exclude: [],
      };
   }

   return JSON.parse(fs.readFileSync(configPath, 'utf8'));
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
   return patterns.some((pattern) => globToRegExp(pattern).test(relativePath));
}

function walkFiles(dir, predicate, files = []) {
   if (!fs.existsSync(dir)) {
      return files;
   }

   fs.readdirSync(dir, { withFileTypes: true }).forEach((entry) => {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
         walkFiles(fullPath, predicate, files);
         return;
      }

      if (entry.isFile() && predicate(fullPath)) {
         files.push(toPosix(path.relative(ROOT, fullPath)));
      }
   });

   return files;
}

function isFlatTestPath(relativePath) {
   const rel = relativePath.slice('tests/scripts/'.length);
   return !rel.includes('/');
}

function main() {
   const oneClass = loadConfig(ONE_CLASS_CONFIG);
   const unitTest = loadConfig(UNIT_TEST_CONFIG);

   const scripts = walkFiles(
      path.join(ROOT, 'scripts'),
      (fullPath) => fullPath.endsWith('.js')
   ).sort();
   const tests = walkFiles(
      path.join(ROOT, 'tests/scripts'),
      (fullPath) => fullPath.endsWith('.test.mjs')
   ).sort();

   const scriptExclude = oneClass.exclude ?? [];
   const scriptInclude = oneClass.include ?? [];
   const scriptCandidates = scripts.filter((file) => !matchesAny(file, scriptExclude));
   const scriptsConverted = scriptCandidates.filter((file) => matchesAny(file, scriptInclude));
   const scriptsRemaining = scriptCandidates.length - scriptsConverted.length;

   const testExclude = unitTest.exclude ?? [];
   const testInclude = unitTest.include ?? [];
   const testCandidates = tests.filter((file) => !matchesAny(file, testExclude));
   const testsStyled = testCandidates.filter((file) => matchesAny(file, testInclude));
   const flatTests = testCandidates.filter(isFlatTestPath);
   const nestedTests = testCandidates.filter((file) => !isFlatTestPath(file));
   const flatTestsRemaining = flatTests.filter((file) => !matchesAny(file, testInclude));

   console.log('JS class / test-style progress');
   console.log(
      `  scripts: ${scriptsConverted.length}/${scriptCandidates.length} under one-class lint`
      + ` (${scriptsRemaining} remaining; ${scriptExclude.length} excluded patterns)`
   );
   console.log(
      `  tests:   ${testsStyled.length}/${testCandidates.length} under unit-test-style lint`
      + ` (${flatTestsRemaining.length} flat remaining; ${nestedTests.length} nested)`
   );

   return 0;
}

process.exit(main());

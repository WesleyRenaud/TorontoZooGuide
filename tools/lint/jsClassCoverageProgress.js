import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const ROOT = process.cwd();
const UNIT_TEST_CONFIG = path.join(ROOT, 'tools/lint/jsUnitTestStyle.json');
const WEAK_NAMES_CONFIG = path.join(ROOT, 'tools/lint/jsWeakClassNames.json');

const DEFAULT_WEAK_NAMES = [
   'View',
   'Shell',
   'State',
   'Popup',
   'Dom',
   'Controllers',
   'Refs',
   'Controls',
   'Sources',
   'Updater',
   'Panels',
   'Format',
   'Rows',
   'Section',
   'Summary',
   'Status',
   'Loaders',
   'Dropdowns',
   'Constants',
];

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

function topLevelExportedClassNames(source) {
   const names = [];
   const classPattern = /^export\s+class\s+([A-Za-z_$][\w$]*)/gm;
   let match = classPattern.exec(source);

   while (match) {
      names.push(match[1]);
      match = classPattern.exec(source);
   }

   return names;
}

function hasTopLevelFunction(source) {
   return /^(?:async\s+)?function\s+[A-Za-z_$]/gm.test(source);
}

function main() {
   const unitTest = loadConfig(UNIT_TEST_CONFIG);
   const weakConfig = loadConfig(WEAK_NAMES_CONFIG);
   const weakNames = new Set(weakConfig.names ?? DEFAULT_WEAK_NAMES);

   const scripts = walkFiles(
      path.join(ROOT, 'scripts'),
      (fullPath) => fullPath.endsWith('.js')
   ).sort();
   const tests = walkFiles(
      path.join(ROOT, 'tests/scripts'),
      (fullPath) => fullPath.endsWith('.test.mjs')
   ).sort();

   const scriptCandidates = scripts;

   const testExclude = unitTest.exclude ?? [];
   const testInclude = unitTest.include ?? [];
   const testCandidates = tests.filter((file) => !matchesAny(file, testExclude));
   const testsStyled = testInclude.length === 0
      ? testCandidates
      : testCandidates.filter((file) => matchesAny(file, testInclude));
   const flatTests = testCandidates.filter(isFlatTestPath);
   const nestedTests = testCandidates.filter((file) => !isFlatTestPath(file));
   const flatTestsRemaining = testInclude.length === 0
      ? []
      : flatTests.filter((file) => !matchesAny(file, testInclude));

   let classPure = 0;
   let withHelpers = 0;
   const classNameToFiles = new Map();
   const weakHits = [];

   scriptCandidates.forEach((relativePath) => {
      const source = fs.readFileSync(path.join(ROOT, relativePath), 'utf8');
      const classNames = topLevelExportedClassNames(source);
      const hasHelpers = hasTopLevelFunction(source);

      if (classNames.length === 1 && !hasHelpers) {
         classPure += 1;
      }
      else if (hasHelpers) {
         withHelpers += 1;
      }

      classNames.forEach((className) => {
         const files = classNameToFiles.get(className) ?? [];
         files.push(relativePath);
         classNameToFiles.set(className, files);

         if (weakNames.has(className)) {
            weakHits.push(`${className} (${relativePath})`);
         }
      });
   });

   const collisions = [...classNameToFiles.entries()]
      .filter(([, files]) => files.length > 1)
      .sort(([left], [right]) => left.localeCompare(right));

   console.log('JS class / test-style progress');
   console.log(`  scripts: ${scriptCandidates.length} one-class (all scripts)`);
   console.log(
      `  tests:   ${testsStyled.length}/${testCandidates.length} under unit-test-style lint`
      + ` (${flatTestsRemaining.length} flat remaining; ${nestedTests.length} nested)`
   );
   console.log('JS class hygiene progress');
   console.log(
      `  class-pure: ${classPure}/${scriptCandidates.length}`
      + ` (${withHelpers} with top-level helpers remaining)`
   );

   if (collisions.length === 0) {
      console.log('  unique-names: OK');
   }
   else {
      console.log(`  unique-names: ${collisions.length} collision(s)`);
      collisions.forEach(([className, files]) => {
         console.log(`    ${className}: ${files.join(', ')}`);
      });
   }

   console.log(`  weak-names: ${weakHits.length} remaining`);

   if (weakHits.length > 0 && weakHits.length <= 40) {
      weakHits.sort().forEach((hit) => {
         console.log(`    ${hit}`);
      });
   }

   return 0;
}

process.exit(main());

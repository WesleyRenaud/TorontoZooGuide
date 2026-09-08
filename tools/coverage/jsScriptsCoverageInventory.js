import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '../..');
const EXCLUDES_PATH = path.join(ROOT, 'tools/coverage/jsCoverageExcludes.json');

function toPosix(filePath) {
   return filePath.split(path.sep).join('/');
}

function globToRegExp(pattern) {
   const escaped = pattern
      .replace(/[.+^${}()|[\]\\]/g, '\\$&')
      .replace(/\*\*/g, '::DOUBLESTAR::')
      .replace(/\*/g, '[^/]*')
      // Node-style ** may span zero path segments (e.g. scripts/**/*Bootstrap.js).
      .replace(/\/::DOUBLESTAR::\//g, '/(?:.*/)?')
      .replace(/::DOUBLESTAR::/g, '.*');

   return new RegExp(`^${escaped}$`);
}

function loadExcludePatterns() {
   const config = JSON.parse(fs.readFileSync(EXCLUDES_PATH, 'utf8'));
   return (config.exclude ?? []).map(globToRegExp);
}

function walkJsFiles(dir, files = []) {
   if (!fs.existsSync(dir)) {
      return files;
   }

   for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
         walkJsFiles(fullPath, files);
         continue;
      }

      if (entry.isFile() && entry.name.endsWith('.js')) {
         files.push(fullPath);
      }
   }

   return files;
}

export function listIncludedScriptPaths() {
   const excludePatterns = loadExcludePatterns();
   const scriptsDir = path.join(ROOT, 'scripts');

   return walkJsFiles(scriptsDir)
      .map((fullPath) => toPosix(path.relative(ROOT, fullPath)))
      .filter((relativePath) => !excludePatterns.some((pattern) => pattern.test(relativePath)))
      .sort();
}

export function mirroredTestPathForScript(scriptPath) {
   return scriptPath
      .replace(/^scripts\//, 'tests/scripts/')
      .replace(/\.js$/, '.test.mjs');
}

export function hasMirroredTest(scriptPath) {
   return fs.existsSync(path.join(ROOT, mirroredTestPathForScript(scriptPath)));
}

/**
 * Parse Node's experimental test coverage table into
 * Map<scriptPath, linePercent>. Files never loaded are absent (treat as 0%).
 */
export function parseCoverageLinePercents(output) {
   const linePercents = new Map();
   const stack = [];

   for (const rawLine of output.split('\n')) {
      if (!rawLine.startsWith('ℹ')) {
         continue;
      }

      const body = rawLine.slice(1);
      const match = body.match(/^(\s*)([^|]+?)\s*\|(.*)$/);

      if (!match) {
         continue;
      }

      const indent = match[1].length;
      const name = match[2].trim();
      const stats = match[3];

      if (!name || name === 'file' || name === 'all files' || name.startsWith('-')) {
         continue;
      }

      while (stack.length > indent - 1) {
         stack.pop();
      }

      if (name.endsWith('.js')) {
         const lineMatch = stats.match(/^\s*([\d.]+)\s*\|/);

         if (!lineMatch) {
            continue;
         }

         const scriptPath = [...stack, name].join('/');
         linePercents.set(scriptPath, Number.parseFloat(lineMatch[1]));
         continue;
      }

      stack.push(name);
   }

   return linePercents;
}

export function buildScriptsCoverageProgress(coverageOutput = '') {
   const includedScripts = listIncludedScriptPaths();
   const linePercents = parseCoverageLinePercents(coverageOutput);

   let withMirroredTest = 0;
   let fullyLineCovered = 0;
   let mirroredAndFullyCovered = 0;
   const missingMirroredTests = [];
   const mirroredButIncomplete = [];

   for (const scriptPath of includedScripts) {
      const mirrored = hasMirroredTest(scriptPath);
      const linePercent = linePercents.get(scriptPath) ?? 0;
      const fullyCovered = linePercent === 100;

      if (mirrored) {
         withMirroredTest += 1;
      } else {
         missingMirroredTests.push(scriptPath);
      }

      if (fullyCovered) {
         fullyLineCovered += 1;
      }

      if (mirrored && fullyCovered) {
         mirroredAndFullyCovered += 1;
      } else if (mirrored) {
         mirroredButIncomplete.push({
            scriptPath,
            linePercent,
         });
      }
   }

   const total = includedScripts.length;

   return {
      total,
      withMirroredTest,
      fullyLineCovered,
      mirroredAndFullyCovered,
      missingMirroredTests,
      mirroredButIncomplete,
      percent(count) {
         if (total === 0) {
            return '0.0';
         }

         return ((count / total) * 100).toFixed(1);
      },
   };
}

export function formatScriptsCoverageProgress(progress, { sampleLimit = 8 } = {}) {
   const lines = [
      'Scripts coverage progress (included scripts):',
      `  Mirrored test files:     ${progress.withMirroredTest}/${progress.total}`
         + ` (${progress.percent(progress.withMirroredTest)}%)`,
      `  Fully line-covered:      ${progress.fullyLineCovered}/${progress.total}`
         + ` (${progress.percent(progress.fullyLineCovered)}%)`,
      `  Mirrored + fully covered: ${progress.mirroredAndFullyCovered}/${progress.total}`
         + ` (${progress.percent(progress.mirroredAndFullyCovered)}%)`,
   ];

   if (progress.missingMirroredTests.length > 0) {
      lines.push('  Missing mirrored tests (sample):');
      for (const scriptPath of progress.missingMirroredTests.slice(0, sampleLimit)) {
         lines.push(`    - ${scriptPath}`);
      }
   }

   if (progress.mirroredButIncomplete.length > 0) {
      lines.push('  Mirrored but not fully covered (sample):');
      for (const { scriptPath, linePercent } of progress.mirroredButIncomplete.slice(0, sampleLimit)) {
         lines.push(`    - ${scriptPath} (${linePercent.toFixed(2)}% lines)`);
      }
   }

   return lines.join('\n');
}

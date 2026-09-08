import { spawn } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
   buildScriptsCoverageProgress,
   formatScriptsCoverageProgress,
} from './jsScriptsCoverageInventory.js';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '../..');
const EXCLUDES = JSON.parse(
   readFileSync(join(ROOT, 'tools/coverage/jsCoverageExcludes.json'), 'utf8')
).exclude ?? [];

const args = [
   '--test',
   '--experimental-test-coverage',
   '--test-coverage-include=scripts/**/*.js',
   ...EXCLUDES.flatMap((pattern) => [`--test-coverage-exclude=${pattern}`]),
   'tests/scripts/**/*.test.mjs',
];

const child = spawn(process.execPath, args, {
   cwd: ROOT,
   stdio: ['inherit', 'pipe', 'pipe'],
});

let output = '';

child.stdout.on('data', (chunk) => {
   const text = chunk.toString();
   output += text;
   process.stdout.write(text);
});

child.stderr.on('data', (chunk) => {
   const text = chunk.toString();
   output += text;
   process.stderr.write(text);
});

child.on('exit', (code, signal) => {
   if (signal) {
      process.kill(process.pid, signal);
      return;
   }

   const progress = buildScriptsCoverageProgress(output);
   console.log(`\n${formatScriptsCoverageProgress(progress)}\n`);

   process.exit(code ?? 1);
});

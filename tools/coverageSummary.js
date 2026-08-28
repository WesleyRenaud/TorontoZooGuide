import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const SUMMARY_FILE = join(tmpdir(), 'tzg-coverage-summary.json');
const MINIMUM_COVERAGE_PERCENT = 80;

// TODO(api-test-migration): When tests/api is the sole Python test tree and all api/
// modules are migrated, change coverage:py to --cov=api (drop per-module paths) and
// update pyproject.toml [tool.coverage.run] source to match.

const COVERAGE_COMMANDS = [
   {
      label: 'API',
      script: 'coverage:py',
      parseCoverage: parseBackendCoverage,
   },
   {
      label: 'Frontend',
      script: 'coverage:js',
      parseCoverage: parseFrontendCoverage,
   },
];

function runNpmScript(script) {
   return new Promise((resolve, reject) => {
      const child = spawn('npm', ['run', script], {
         stdio: ['inherit', 'pipe', 'pipe'],
      });
      let output = '';

      child.stdout.on('data', chunk => {
         output += chunk.toString();
         process.stdout.write(chunk);
      });

      child.stderr.on('data', chunk => {
         output += chunk.toString();
         process.stderr.write(chunk);
      });

      child.on('error', reject);
      child.on('close', code => {
         resolve({ code, output });
      });
   });
}

function parseBackendCoverage(output) {
   const matches = [...output.matchAll(/^TOTAL\s+\d+\s+\d+\s+([\d.]+%)/gm)];
   const lastMatch = matches.at(-1);

   return parseCoveragePercent(lastMatch?.[1] ?? null);
}

function parseFrontendCoverage(output) {
   const matches = [...output.matchAll(/all files\s+\|\s+([\d.]+)\s+\|/g)];
   const lastMatch = matches.at(-1);

   return parseCoveragePercent(lastMatch ? `${ lastMatch[1] }%` : null);
}

function parseCoveragePercent(value) {
   if (!value) {
      return null;
   }

   const percent = Number.parseFloat(value);

   if (!Number.isFinite(percent)) {
      return null;
   }

   return {
      display: value,
      percent,
   };
}

function printCoverageSummary(summary) {
   console.log('\nCoverage summary:');

   for (const { label, coverage } of summary) {
      console.log(`${ label }: ${ coverage?.display ?? 'unavailable' }`);
   }
}

function printCoverageThresholdFailures(summary) {
   const failures = summary.filter(({ coverage }) => (
      !coverage || coverage.percent < MINIMUM_COVERAGE_PERCENT
   ));

   if (!failures.length) {
      return false;
   }

   console.error(`\nCoverage threshold failed. Minimum required: ${ MINIMUM_COVERAGE_PERCENT }%.`);

   for (const { label, coverage } of failures) {
      console.error(`${ label }: ${ coverage?.display ?? 'unavailable' }`);
   }

   return true;
}

function writeCoverageSummary(summary) {
   writeFileSync(SUMMARY_FILE, JSON.stringify(summary), 'utf8');
}

if (process.argv.includes('--print-last-summary')) {
   const summary = JSON.parse(readFileSync(SUMMARY_FILE, 'utf8'));

   printCoverageSummary(summary);
   process.exit(0);
}

const summary = [];
let exitCode = 0;

for (const command of COVERAGE_COMMANDS) {
   const result = await runNpmScript(command.script);
   const coverage = command.parseCoverage(result.output);

   summary.push({
      label: command.label,
      coverage,
   });

   if (result.code !== 0) {
      exitCode = result.code;
      break;
   }
}

writeCoverageSummary(summary);
printCoverageSummary(summary);

if (exitCode === 0 && printCoverageThresholdFailures(summary)) {
   exitCode = 1;
}

process.exit(exitCode);

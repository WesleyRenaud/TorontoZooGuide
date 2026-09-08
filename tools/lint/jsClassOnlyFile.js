import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const ROOT = process.cwd();

function toPosix(filePath) {
   return filePath.split(path.sep).join('/');
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

function stripComments(source) {
   let out = '';
   let i = 0;
   let state = 'code';

   while (i < source.length) {
      const c = source[i];
      const n = source[i + 1];

      if (state === 'code') {
         if (c === '/' && n === '/') {
            out += '  ';
            i += 2;
            while (i < source.length && source[i] !== '\n') {
               out += ' ';
               i++;
            }
            continue;
         }
         if (c === '/' && n === '*') {
            out += '  ';
            i += 2;
            while (i < source.length && !(source[i] === '*' && source[i + 1] === '/')) {
               out += source[i] === '\n' ? '\n' : ' ';
               i++;
            }
            out += '  ';
            i += 2;
            continue;
         }
         if (c === "'") {
            state = 'squote';
            out += c;
            i++;
            continue;
         }
         if (c === '"') {
            state = 'dquote';
            out += c;
            i++;
            continue;
         }
         if (c === '`') {
            state = 'template';
            out += c;
            i++;
            continue;
         }
         out += c;
         i++;
         continue;
      }

      if (state === 'squote') {
         out += c;
         if (c === '\\') {
            out += source[++i] || '';
            i++;
            continue;
         }
         if (c === "'") {
            state = 'code';
         }
         i++;
         continue;
      }

      if (state === 'dquote') {
         out += c;
         if (c === '\\') {
            out += source[++i] || '';
            i++;
            continue;
         }
         if (c === '"') {
            state = 'code';
         }
         i++;
         continue;
      }

      if (state === 'template') {
         out += c;
         if (c === '\\') {
            out += source[++i] || '';
            i++;
            continue;
         }
         if (c === '`') {
            state = 'code';
            i++;
            continue;
         }
         i++;
      }
   }

   return out;
}

function matchBrace(source, openIdx) {
   let depth = 0;

   for (let i = openIdx; i < source.length; i++) {
      const c = source[i];

      if (c === '{') {
         depth++;
      } else if (c === '}') {
         depth--;
         if (depth === 0) {
            return i;
         }
      }
   }

   return -1;
}

function checkFile(fullPath) {
   const relativePath = toPosix(path.relative(ROOT, fullPath));
   const source = fs.readFileSync(fullPath, 'utf8');
   const stripped = stripComments(source);
   const lines = stripped.split('\n');
   const violations = [];

   let phase = 'imports';
   let inImport = false;
   let classLineIndex = -1;
   let classOpenIndex = -1;

   for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();

      if (!trimmed) {
         continue;
      }

      if (phase === 'imports') {
         if (inImport) {
            if (trimmed.includes(';')) {
               inImport = false;
            }
            continue;
         }

         if (/^import\b/.test(trimmed)) {
            if (!trimmed.includes(';')) {
               inImport = true;
            }
            continue;
         }

         if (/^export\s+class\b/.test(trimmed)) {
            phase = 'class';
            classLineIndex = i;
            classOpenIndex = stripped.indexOf('{', lines.slice(0, i).join('\n').length);
            continue;
         }

         violations.push(
            `${relativePath}:${i + 1}: expected import or export class; found module-level code`
         );
         return violations;
      }
   }

   if (classLineIndex < 0) {
      violations.push(`${relativePath}: expected exactly one export class`);
      return violations;
   }

   if (classOpenIndex < 0) {
      violations.push(`${relativePath}: could not find class body`);
      return violations;
   }

   const classCloseIndex = matchBrace(stripped, classOpenIndex);
   if (classCloseIndex < 0) {
      violations.push(`${relativePath}: could not find end of class body`);
      return violations;
   }

   const afterClass = stripped.slice(classCloseIndex + 1);
   const afterTrimmed = afterClass.trim();
   if (afterTrimmed) {
      const afterLine = stripped.slice(0, classCloseIndex).split('\n').length + 1;
      violations.push(
         `${relativePath}:${afterLine}: module-level code after class is not allowed`
      );
   }

   const beforeClass = stripped.slice(0, lines.slice(0, classLineIndex).join('\n').length);
   const forbiddenBefore = /(?:^|\n)\s*(?:export\s+)?(?:const|let|var|function|async\s+function|class)\b/.exec(
      beforeClass
   );
   if (forbiddenBefore) {
      const line = beforeClass.slice(0, forbiddenBefore.index).split('\n').length;
      violations.push(
         `${relativePath}:${line}: module-level binding/declaration is not allowed; use class statics`
      );
   }

   const exportCount = [...stripped.matchAll(/(?:^|\n)\s*export\b/g)].length;
   if (exportCount !== 1) {
      violations.push(
         `${relativePath}: expected exactly one export (the class), found ${exportCount}`
      );
   }

   const classExports = [...stripped.matchAll(/(?:^|\n)\s*export\s+class\b/g)];
   if (classExports.length !== 1) {
      violations.push(
         `${relativePath}: expected exactly one export class, found ${classExports.length}`
      );
   }

   return violations;
}

function main() {
   const scriptsDir = path.join(ROOT, 'scripts');
   const violations = [];

   walkJsFiles(scriptsDir).forEach(fullPath => {
      violations.push(...checkFile(fullPath));
   });

   if (violations.length === 0) {
      return 0;
   }

   violations.forEach(violation => {
      console.error(violation);
   });
   console.error(`\nFound ${violations.length} class-only-file violation(s).`);
   return 1;
}

process.exit(main());

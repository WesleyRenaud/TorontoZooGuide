import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const rootDir = path.resolve('scripts');
const shouldFix = process.argv.includes('--fix');
const violations = [];

function walk(dir) {
   const entries = fs.readdirSync(dir, { withFileTypes: true });

   entries.forEach(entry => {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
         walk(fullPath);
         return;
      }

      if (entry.isFile() && entry.name.endsWith('.js')) {
         checkFile(fullPath);
      }
   });
}

function getLeadingImportBlock(source) {
   let cursor = 0;
   const declarations = [];

   while (cursor < source.length) {
      const whitespace = source.slice(cursor).match(/^\s*/)?.[0] ?? '';
      const importStart = cursor + whitespace.length;

      if (!source.startsWith('import ', importStart)) {
         break;
      }

      const declarationEnd = source.indexOf(';', importStart);

      if (declarationEnd === -1) {
         break;
      }

      declarations.push(source.slice(importStart, declarationEnd + 1));
      cursor = declarationEnd + 1;
   }

   if (declarations.length === 0) {
      return null;
   }

   return {
      endIndex: cursor,
      declarations,
   };
}

function getImportSource(declaration) {
   return declaration.match(/\sfrom\s+['"]([^'"]+)['"]/)?.[1] ?? declaration;
}

function getImportSortKey(declaration) {
   const source = getImportSource(declaration);
   const importedNames = getNamedImports(declaration);
   const firstImport = importedNames[0] ?? declaration;
   const normalizedSource = source.replace(/^(\.\.\/|\.\/)+/, '');

   return `${normalizedSource.toLowerCase()}\0${firstImport.toLowerCase()}`;
}

function getNamedImports(declaration) {
   const namedImportBody = declaration.match(/import\s*{\s*([\s\S]*?)\s*}\s*from/)?.[1];

   if (!namedImportBody) {
      return [];
   }

   return namedImportBody
      .split(',')
      .map(value => value.trim())
      .filter(Boolean);
}

function sortNamedImports(imports) {
   return [...imports].sort((left, right) => (
      left.toLowerCase().localeCompare(right.toLowerCase())
   ));
}

function formatNamedImportDeclaration(declaration) {
   const match = declaration.match(/import\s*{\s*([\s\S]*?)\s*}\s*from\s*(['"][^'"]+['"])/);

   if (!match) {
      return declaration.trim();
   }

   const namedImports = sortNamedImports(getNamedImports(declaration));
   const source = match[2];

   if (namedImports.length === 1) {
      return `import { ${namedImports[0]} } from ${source};`;
   }

   return [
      'import {',
      ...namedImports.map(name => `   ${name},`),
      `} from ${source};`,
   ].join('\n');
}

function formatImportBlock(declarations) {
   return declarations
      .map(formatNamedImportDeclaration)
      .sort((left, right) => getImportSortKey(left).localeCompare(getImportSortKey(right)))
      .join('\n');
}

function checkFile(fullPath) {
   const source = fs.readFileSync(fullPath, 'utf8');
   const importBlock = getLeadingImportBlock(source);

   if (!importBlock) {
      return;
   }

   const currentBlock = source.slice(0, importBlock.endIndex).trim();
   const expectedBlock = formatImportBlock(importBlock.declarations);

   if (currentBlock === expectedBlock) {
      return;
   }

   const relativePath = path.relative(process.cwd(), fullPath);
   violations.push(relativePath);

   if (shouldFix) {
      const rest = source.slice(importBlock.endIndex).replace(/^\s*/, '\n\n');
      fs.writeFileSync(fullPath, `${expectedBlock}${rest}`, 'utf8');
   }
}

walk(rootDir);

if (violations.length > 0 && !shouldFix) {
   console.error('JavaScript imports must be alphabetized and use project brace layout:');
   violations.forEach(file => {
      console.error(file);
   });
   console.error('Run `node tools/lint/jsImportStyle.js --fix` to update imports.');
   process.exit(1);
}

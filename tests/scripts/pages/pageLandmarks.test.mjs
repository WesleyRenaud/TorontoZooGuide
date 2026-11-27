import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';

const PAGES_DIR = new URL('../../../pages/', import.meta.url);
const ALL_PAGES = ['map.html', 'itinerary.html', 'animals.html', 'console-operations.html'];
const PAGES_WITH_NAV = ['map.html', 'itinerary.html', 'animals.html'];

function _readPage(fileName) {
   return fs.readFileSync(new URL(fileName, PAGES_DIR), 'utf8');
}

function _countMatches(source, pattern) {
   return (source.match(pattern) ?? []).length;
}


test('Test_StaticMarkup_TestEveryPage_ExpectOneH1InsideTopBarHeader', () => {
   ALL_PAGES.forEach((fileName) => {
      const html = _readPage(fileName);
      const header = html.match(/<header class="top-bar">([\s\S]*?)<\/header>/);

      assert.equal(_countMatches(html, /<h1[\s>]/g), 1, fileName);
      assert.ok(header, `${fileName} top bar should be a header element`);
      assert.match(header[1], /<h1 class="top-bar-title">/, fileName);
   });
});


test('Test_StaticMarkup_TestEveryPage_ExpectExactlyOneMain', () => {
   ALL_PAGES.forEach((fileName) => {
      assert.equal(_countMatches(_readPage(fileName), /<main[\s>]/g), 1, fileName);
   });
});


test('Test_StaticMarkup_TestPagesWithNav_ExpectOneNamedNav', () => {
   PAGES_WITH_NAV.forEach((fileName) => {
      const html = _readPage(fileName);

      assert.equal(_countMatches(html, /<nav[\s>]/g), 1, fileName);
      assert.match(html, /<nav aria-label="\{\{ site\.nav\.ariaLabel \}\}">/, fileName);
   });
});

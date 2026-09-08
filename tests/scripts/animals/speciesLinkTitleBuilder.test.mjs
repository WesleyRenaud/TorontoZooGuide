import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesLinkTitleBuilder } from '../../../scripts/animals/speciesLinkTitleBuilder.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateSpeciesLinkTitleElement_TestPlainText_ExpectTitleWithoutLinkRole', () => {
   const titleEl = SpeciesLinkTitleBuilder.createSpeciesLinkTitleElement({
      text: 'African Lion',
      className: 'animal-title',
   });
   const linkEl = titleEl.children[0];

   assert.equal(titleEl.className, 'animal-title');
   assert.equal(titleEl.textContent, 'African Lion');
   assert.equal(linkEl.classList.contains('species-link'), false);
});

test('Test_CreateSpeciesLinkTitleElement_TestDatasetLink_ExpectSpeciesLink', () => {
   const titleEl = SpeciesLinkTitleBuilder.createSpeciesLinkTitleElement({
      text: 'African Lion',
      dataset: { species: 'African Lion' },
      suffix: ' • Outdoor',
   });
   const linkEl = titleEl.children[0];

   assert.equal(linkEl.classList.contains('species-link'), true);
   assert.equal(linkEl.dataset.species, 'African Lion');
   assert.match(titleEl.textContent, /African Lion/);
   assert.match(titleEl.textContent, /Outdoor/);
});

test('Test_CreateAnimalTitleLinkElement_TestEnclosureSuffix_ExpectFormattedTitle', () => {
   const titleEl = SpeciesLinkTitleBuilder.createAnimalTitleLinkElement({
      species: 'African Lion',
      enclosureName: 'African Savanna',
      onClick: () => {},
   });
   const linkEl = titleEl.children[0];

   assert.match(titleEl.textContent, /African Lion/);
   assert.match(titleEl.textContent, /African Savanna/);
   assert.equal(linkEl.classList.contains('species-link'), true);
});

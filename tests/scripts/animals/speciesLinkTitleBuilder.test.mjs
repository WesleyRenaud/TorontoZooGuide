import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesLinkTitleBuilder } from '../../../scripts/animals/speciesLinkTitleBuilder.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateSpeciesLinkTitleElement_TestPlainText_ExpectTitleWithoutLinkRole', () => {
   const text = 'African Lion';
   const className = 'animal-title';

   const titleEl = SpeciesLinkTitleBuilder.createSpeciesLinkTitleElement({
      text,
      className,
   });
   const linkEl = titleEl.children.at(Position.FIRST);

   assert.equal(titleEl.className, className);
   assert.equal(titleEl.textContent, text);
   assert.equal(linkEl.classList.contains('species-link'), false);
});


test('Test_CreateSpeciesLinkTitleElement_TestDatasetLink_ExpectSpeciesLink', () => {
   const text = 'African Lion';
   const suffix = ' • Outdoor';

   const titleEl = SpeciesLinkTitleBuilder.createSpeciesLinkTitleElement({
      text,
      dataset: { species: text },
      suffix,
   });
   const linkEl = titleEl.children.at(Position.FIRST);

   assert.equal(linkEl.classList.contains('species-link'), true);
   assert.equal(linkEl.dataset.species, text);
   assert.match(titleEl.textContent, new RegExp(text));
   assert.match(titleEl.textContent, /Outdoor/);
});


test('Test_CreateAnimalTitleLinkElement_TestEnclosureSuffix_ExpectFormattedTitle', () => {
   const species = 'African Lion';
   const enclosureName = 'African Savanna';

   const titleEl = SpeciesLinkTitleBuilder.createAnimalTitleLinkElement({
      species,
      enclosureName,
      onClick: () => {},
   });
   const linkEl = titleEl.children.at(Position.FIRST);

   assert.match(titleEl.textContent, new RegExp(species));
   assert.match(titleEl.textContent, new RegExp(enclosureName));
   assert.equal(linkEl.classList.contains('species-link'), true);
});

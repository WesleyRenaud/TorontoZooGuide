import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesOverlayModal } from '../../../scripts/overlays/speciesOverlayModal.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_GetSpeciesTitle_TestMissingDialog_ExpectNull', () => {
   assert.equal(SpeciesOverlayModal.getSpeciesTitle(null), null);
   assert.equal(SpeciesOverlayModal.getSpeciesTitle(createDomNode('div')), null);
});


test('Test_DecorateSpeciesDialog_TestMissingTitle_ExpectNoRegion', () => {
   const dialog = createDomNode('div', 'species-overlay-card');
   const scroll = createDomNode('div', 'species-overlay-scroll');
   dialog.appendChild(scroll);

   SpeciesOverlayModal.decorateSpeciesDialog(dialog, null);

   assert.equal(scroll.getAttribute('role'), null);
   assert.equal(scroll.getAttribute('tabindex'), null);
});


test('Test_DecorateSpeciesDialog_TestTitleWithoutScroll_ExpectTitleUnchanged', () => {
   const dialog = createDomNode('div', 'species-overlay-card');
   const title = createDomNode('h2', 'animal-species-name');
   dialog.appendChild(title);

   SpeciesOverlayModal.decorateSpeciesDialog(dialog, title);

   assert.equal(dialog.querySelector('.species-overlay-scroll'), null);
   assert.equal(title.getAttribute('tabindex'), null);
});

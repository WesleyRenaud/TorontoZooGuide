import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesOverlayBuilder } from '../../../scripts/overlays/speciesOverlayBuilder.js';
import { SpeciesOverlayView } from '../../../scripts/overlays/speciesOverlayView.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ResolveOverlayElements_TestMissing_ExpectNulls', () => {
   assert.deepEqual(SpeciesOverlayBuilder.resolveOverlayElements(), {
      overlay: null,
      content: null,
      closeButton: null,
   });
});

test('Test_ResolveOverlayElements_TestPresent_ExpectParts', () => {
   const overlay = document.createElement('div');
   overlay.id = 'speciesOverlay';
   const content = document.createElement('div');
   content.className = 'species-overlay-content';
   const closeButton = document.createElement('button');
   closeButton.className = 'species-close';
   overlay.append(content, closeButton);

   const originalGet = document.getElementById;
   document.getElementById = (id) => (id === 'speciesOverlay' ? overlay : null);

   try {
      const parts = SpeciesOverlayBuilder.resolveOverlayElements();
      assert.equal(parts.overlay, overlay);
      assert.equal(parts.content, content);
      assert.equal(parts.closeButton, closeButton);
   } finally {
      document.getElementById = originalGet;
   }
});

test('Test_FindLinkedAnimalIndex_TestMatch_ExpectIndex', () => {
   const linkedAnimals = [
      { species: 'African Lion', exhibit: 'African Savanna' },
      { species: 'Amur Tiger', exhibit: 'Eurasia' },
   ];

   assert.equal(
      SpeciesOverlayBuilder.findLinkedAnimalIndex(linkedAnimals, {
         species: 'Amur Tiger',
         exhibit: 'Eurasia',
      }),
      1
   );
   assert.equal(
      SpeciesOverlayBuilder.findLinkedAnimalIndex(linkedAnimals, {
         species: 'Giraffe',
         exhibit: 'African Savanna',
      }),
      -1
   );
});

test('Test_CreateNavButton_TestClick_ExpectHandler', () => {
   const clicks = [];
   const button = SpeciesOverlayBuilder.createNavButton({
      className: 'nav',
      label: 'Next',
      symbol: '>',
      onClick: () => { clicks.push(true); },
   });

   assert.equal(button.getAttribute('aria-label'), 'Next');
   assert.equal(button.textContent, '>');
   button.listeners.click({ stopPropagation() {} });
   assert.deepEqual(clicks, [true]);
});

test('Test_CreateOverlayHeader_TestSingleAnimal_ExpectEmptyHeader', () => {
   const header = SpeciesOverlayBuilder.createOverlayHeader({
      linkedAnimals: [{ species: 'Lion' }],
      index: 0,
      onNavigate: () => {},
   });

   assert.equal(header.className, 'species-overlay-header');
   assert.equal(header.children.length, 0);
});

test('Test_CreateOverlayHeader_TestMultipleAnimals_ExpectNav', () => {
   const navigations = [];
   const header = SpeciesOverlayBuilder.createOverlayHeader({
      linkedAnimals: [{ species: 'Lion' }, { species: 'Tiger' }],
      index: 0,
      onNavigate: (delta) => { navigations.push(delta); },
   });

   assert.match(header.textContent, new RegExp(Strings.common.animalPosition(1, 2)));
   header.querySelector('.species-overlay-nav-next').listeners.click({ stopPropagation() {} });
   assert.deepEqual(navigations, [1]);
});

test('Test_CreateOverlayScrollContent_TestAnimal_ExpectScroll', () => {
   const original = SpeciesOverlayView.buildSpeciesContent;
   SpeciesOverlayView.buildSpeciesContent = () => {
      const node = document.createElement('div');
      node.className = 'species-content';
      return node;
   };

   try {
      const scroll = SpeciesOverlayBuilder.createOverlayScrollContent({ species: 'Lion' });
      assert.equal(scroll.className, 'species-overlay-scroll');
      assert.equal(scroll.children[0].className, 'species-content');
   } finally {
      SpeciesOverlayView.buildSpeciesContent = original;
   }
});

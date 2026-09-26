import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesOverlayBuilder } from '../../../scripts/overlays/speciesOverlayBuilder.js';
import { SpeciesOverlayView } from '../../../scripts/overlays/speciesOverlayView.js';
import { Strings } from '../../../scripts/strings.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ResolveOverlayElements_TestMissing_ExpectNulls', () => {
   const parts = SpeciesOverlayBuilder.resolveOverlayElements();

   assert.deepEqual(parts, {
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
   document.getElementById = (id) => (id === overlay.id ? overlay : null);

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
   const africanLion = { species: 'African Lion', exhibit: 'African Savanna' };
   const amurTiger = { species: 'Amur Tiger', exhibit: 'Eurasia' };
   const linkedAnimals = [africanLion, amurTiger];

   const index = SpeciesOverlayBuilder.findLinkedAnimalIndex(linkedAnimals, amurTiger);

   assert.equal(index, Position.SECOND);
});


test('Test_FindLinkedAnimalIndex_TestMissing_ExpectLast', () => {
   const linkedAnimals = [
      { species: 'African Lion', exhibit: 'African Savanna' },
      { species: 'Amur Tiger', exhibit: 'Eurasia' },
   ];

   const index = SpeciesOverlayBuilder.findLinkedAnimalIndex(linkedAnimals, {
      species: 'Giraffe',
      exhibit: 'African Savanna',
   });

   assert.equal(index, Position.LAST);
});


test('Test_CreateNavButton_TestClick_ExpectHandler', () => {
   const clicks = [];
   const label = 'Next';
   const symbol = '>';

   const button = SpeciesOverlayBuilder.createNavButton({
      className: 'nav',
      label,
      symbol,
      onClick: () => {
         clicks.push(true);
      },
   });
   button.listeners.click({ stopPropagation() {} });

   assert.equal(button.getAttribute('aria-label'), label);
   assert.equal(button.textContent, symbol);
   assert.deepEqual(clicks, [true]);
});


test('Test_CreateOverlayHeader_TestSingleAnimal_ExpectEmptyHeader', () => {
   const header = SpeciesOverlayBuilder.createOverlayHeader({
      linkedAnimals: [{ species: 'African Lion' }],
      index: Position.FIRST,
      onNavigate: () => {},
   });

   assert.equal(header.className, 'species-overlay-header');
   assert.equal(header.children.length, Position.FIRST);
});


test('Test_CreateOverlayHeader_TestMultipleAnimals_ExpectNav', () => {
   const navigations = [];
   const linkedAnimals = [{ species: 'African Lion' }, { species: 'Amur Tiger' }];

   const header = SpeciesOverlayBuilder.createOverlayHeader({
      linkedAnimals,
      index: Position.FIRST,
      onNavigate: (delta) => {
         navigations.push(delta);
      },
   });
   header.querySelector('.species-overlay-nav-next').listeners.click({ stopPropagation() {} });

   assert.match(header.textContent, new RegExp(Strings.common.animalPosition(1, linkedAnimals.length)));
   assert.deepEqual(navigations, [Position.SECOND]);
});


test('Test_CreateOverlayScrollContent_TestAnimal_ExpectScroll', () => {
   const original = SpeciesOverlayView.buildSpeciesContent;
   SpeciesOverlayView.buildSpeciesContent = () => {
      const node = document.createElement('div');
      node.className = 'species-content';
      return node;
   };

   try {
      const scroll = SpeciesOverlayBuilder.createOverlayScrollContent({ species: 'African Lion' });

      assert.equal(scroll.className, 'species-overlay-scroll');
      assert.equal(scroll.children.at(Position.FIRST).className, 'species-content');
   } finally {
      SpeciesOverlayView.buildSpeciesContent = original;
   }
});

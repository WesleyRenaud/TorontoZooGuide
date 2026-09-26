import assert from 'node:assert/strict';
import test from 'node:test';

import { CreateSpeciesLinkTitleHelper } from '../../../scripts/animals/createSpeciesLinkTitleHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';


function _createLinkElement() {
   const classes = new Set();
   const attributes = {};
   const listeners = {};

   return {
      dataset: {},
      classList: {
         add(value) {
            classes.add(value);
         },
         contains(value) {
            return classes.has(value);
         },
      },
      setAttribute(name, value) {
         attributes[name] = value;
      },
      getAttribute(name) {
         return attributes[name] ?? null;
      },
      addEventListener(name, handler) {
         listeners[name] = handler;
      },
      trigger(name, event) {
         listeners[name]?.(event);
      },
   };
}


test('Test_ApplyLinkDataset_TestValues_ExpectDatasetWritten', () => {
   const species = 'African Lion';
   const element = _createLinkElement();

   CreateSpeciesLinkTitleHelper.applyLinkDataset(element, {
      species,
      exhibit: null,
      unused: undefined,
   });

   assert.equal(element.dataset.species, species);
   assert.equal(element.dataset.exhibit, undefined);
});


test('Test_BindSpeciesLinkActivation_TestClickAndEnter_ExpectCallback', () => {
   const linkEl = _createLinkElement();
   let clicks = Position.FIRST;

   CreateSpeciesLinkTitleHelper.bindSpeciesLinkActivation(linkEl, () => {
      clicks += 1;
   });
   linkEl.trigger('click', {
      stopPropagation() {},
   });
   linkEl.trigger('keydown', {
      key: 'Enter',
      preventDefault() {},
      stopPropagation() {},
   });

   assert.equal(linkEl.classList.contains('species-link'), true);
   assert.equal(linkEl.getAttribute('role'), 'button');
   assert.equal(linkEl.getAttribute('tabindex'), String(Position.FIRST));
   assert.equal(clicks, 2);
});

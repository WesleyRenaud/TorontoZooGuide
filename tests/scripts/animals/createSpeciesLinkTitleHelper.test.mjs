import assert from 'node:assert/strict';
import test from 'node:test';

import { CreateSpeciesLinkTitleHelper } from '../../../scripts/animals/createSpeciesLinkTitleHelper.js';

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
   const element = _createLinkElement();

   CreateSpeciesLinkTitleHelper.applyLinkDataset(element, {
      species: 'African Lion',
      exhibit: null,
      unused: undefined,
   });

   assert.equal(element.dataset.species, 'African Lion');
   assert.equal(element.dataset.exhibit, undefined);
});

test('Test_BindSpeciesLinkActivation_TestClickAndEnter_ExpectCallback', () => {
   const linkEl = _createLinkElement();
   let clicks = 0;

   CreateSpeciesLinkTitleHelper.bindSpeciesLinkActivation(linkEl, () => {
      clicks += 1;
   });

   assert.equal(linkEl.classList.contains('species-link'), true);
   assert.equal(linkEl.getAttribute('role'), 'button');
   assert.equal(linkEl.getAttribute('tabindex'), '0');

   linkEl.trigger('click', {
      stopPropagation() {},
   });
   assert.equal(clicks, 1);

   linkEl.trigger('keydown', {
      key: 'Enter',
      preventDefault() {},
      stopPropagation() {},
   });
   assert.equal(clicks, 2);
});

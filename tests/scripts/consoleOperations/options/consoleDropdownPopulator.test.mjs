import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDropdownOptionBuilder } from '../../../../scripts/consoleOperations/options/consoleDropdownOptionBuilder.js';
import { ConsoleDropdownPopulator } from '../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _select() {
   return document.createElement('select');
}

test('Test_PopulateDropdown_TestNonSelect_ExpectNoOp', () => {
   const originalPlaceholder = ConsoleDropdownOptionBuilder.createPlaceholderOption;
   let called = false;
   ConsoleDropdownOptionBuilder.createPlaceholderOption = () => {
      called = true;
      return document.createElement('option');
   };

   try {
      ConsoleDropdownPopulator.populateDropdown(document.createElement('div'), ['A']);
      ConsoleDropdownPopulator.populateDropdown(null, ['A']);
      assert.equal(called, false);
   } finally {
      ConsoleDropdownOptionBuilder.createPlaceholderOption = originalPlaceholder;
   }
});

test('Test_PopulateDropdown_TestItemsAndSort_ExpectOptions', () => {
   const selectEl = _select();

   ConsoleDropdownPopulator.populateDropdown(selectEl, ['Zebra', '', 'Lion'], {
      emptyOptionLabel: 'Pick one',
      sortItems: (items) => items.slice().reverse(),
   });

   assert.deepEqual(
      selectEl.children.map((option) => [option.value, option.textContent]),
      [
         ['', 'Pick one'],
         ['Lion', 'Lion'],
         ['Zebra', 'Zebra'],
      ]
   );
});

test('Test_PopulateDropdown_TestNullItems_ExpectPlaceholderOnly', () => {
   const selectEl = _select();
   ConsoleDropdownPopulator.populateDropdown(selectEl, null);
   assert.equal(selectEl.children.length, 1);
   assert.equal(selectEl.children[0].textContent, Strings.placeholders.option);
});
test('Test_PopulateValueDropdown_TestValues_ExpectDelegates', () => {
   const selectEl = _select();
   const original = ConsoleDropdownPopulator.populateDropdown;
   let captured;

   ConsoleDropdownPopulator.populateDropdown = (el, values, options) => {
      captured = { el, values, options };
   };

   try {
      ConsoleDropdownPopulator.populateValueDropdown(selectEl, ['A', 'B'], 'Choose');
      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.values, ['A', 'B']);
      assert.deepEqual(captured.options, { emptyOptionLabel: 'Choose' });
   } finally {
      ConsoleDropdownPopulator.populateDropdown = original;
   }
});

test('Test_PopulateNamedDropdowns_TestEntities_ExpectPlaceholders', () => {
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   const calls = [];

   ConsoleDropdownOptionBuilder.populateNamedDropdown = (selectEl, items, emptyOptionLabel) => {
      calls.push({ selectEl, items, emptyOptionLabel });
   };

   const selectEl = _select();

   try {
      ConsoleDropdownPopulator.populateExhibitDropdown(selectEl, [{ name: 'Savanna' }]);
      ConsoleDropdownPopulator.populateRestaurantDropdown(selectEl, [{ name: 'Cafe' }]);
      ConsoleDropdownPopulator.populateRestroomDropdown(selectEl, [{ name: 'Main' }]);
      ConsoleDropdownPopulator.populateGiftShopDropdown(selectEl, [{ name: 'Shop' }]);
      ConsoleDropdownPopulator.populateAttractionDropdown(selectEl, [{ name: 'Carousel' }]);
      ConsoleDropdownPopulator.populateTransportationStationDropdown(selectEl, [{ name: 'Station' }]);
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown(selectEl, [{ name: 'Talk' }]);
      ConsoleDropdownPopulator.populateWildEncounterDropdown(selectEl, [{ name: 'Encounter' }]);

      assert.deepEqual(calls.map((call) => call.emptyOptionLabel), [
         Strings.placeholders.exhibit,
         Strings.placeholders.restaurant,
         Strings.placeholders.restroom,
         Strings.placeholders.giftShop,
         Strings.placeholders.attraction,
         Strings.placeholders.transportationStation,
         Strings.placeholders.talk,
         Strings.placeholders.wildEncounter,
      ]);
      assert.equal(calls.every((call) => call.selectEl === selectEl), true);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});

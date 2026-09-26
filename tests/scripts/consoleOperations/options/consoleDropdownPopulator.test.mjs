import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDropdownOptionBuilder } from '../../../../scripts/consoleOperations/options/consoleDropdownOptionBuilder.js';
import { ConsoleDropdownPopulator } from '../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _select() {
   return document.createElement('select');
}

function _optionPairs(selectEl) {
   return selectEl.children.map((option) => [option.value, option.textContent]);
}


test('Test_PopulateDropdown_TestDiv_ExpectNoOp', () => {
   const originalPlaceholder = ConsoleDropdownOptionBuilder.createPlaceholderOption;
   let called = false;
   ConsoleDropdownOptionBuilder.createPlaceholderOption = () => {
      called = true;
      return document.createElement('option');
   };

   try {
      ConsoleDropdownPopulator.populateDropdown(document.createElement('div'), ['A']);

      assert.equal(called, false);
   } finally {
      ConsoleDropdownOptionBuilder.createPlaceholderOption = originalPlaceholder;
   }
});


test('Test_PopulateDropdown_TestNull_ExpectNoOp', () => {
   const originalPlaceholder = ConsoleDropdownOptionBuilder.createPlaceholderOption;
   let called = false;
   ConsoleDropdownOptionBuilder.createPlaceholderOption = () => {
      called = true;
      return document.createElement('option');
   };

   try {
      ConsoleDropdownPopulator.populateDropdown(null, ['A']);

      assert.equal(called, false);
   } finally {
      ConsoleDropdownOptionBuilder.createPlaceholderOption = originalPlaceholder;
   }
});


test('Test_PopulateDropdown_TestItemsAndSort_ExpectOptions', () => {
   const zebra = 'Zebra';
   const lion = 'Lion';
   const emptyOptionLabel = 'Pick one';
   const items = [zebra, '', lion];
   const selectEl = _select();

   ConsoleDropdownPopulator.populateDropdown(selectEl, items, {
      emptyOptionLabel,
      sortItems: (values) => values.slice().reverse(),
   });

   assert.deepEqual(
      _optionPairs(selectEl),
      [
         ['', emptyOptionLabel],
         [lion, lion],
         [zebra, zebra],
      ]
   );
});


test('Test_PopulateDropdown_TestNullItems_ExpectPlaceholderOnly', () => {
   const selectEl = _select();

   ConsoleDropdownPopulator.populateDropdown(selectEl, null);

   assert.equal(selectEl.children.length, 1);
   assert.equal(
      selectEl.children.at(Position.FIRST).textContent,
      Strings.placeholders.option
   );
});


test('Test_PopulateValueDropdown_TestValues_ExpectDelegates', () => {
   const selectEl = _select();
   const values = ['A', 'B'];
   const emptyOptionLabel = 'Choose';
   const original = ConsoleDropdownPopulator.populateDropdown;
   let captured;
   ConsoleDropdownPopulator.populateDropdown = (el, items, options) => {
      captured = { el, items, options };
   };

   try {
      ConsoleDropdownPopulator.populateValueDropdown(selectEl, values, emptyOptionLabel);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.items, values);
      assert.deepEqual(captured.options, { emptyOptionLabel });
   } finally {
      ConsoleDropdownPopulator.populateDropdown = original;
   }
});


test('Test_PopulateExhibitDropdown_TestEntities_ExpectPlaceholder', () => {
   const name = 'Savanna';
   const items = [{ name }];
   const selectEl = _select();
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   let captured;
   ConsoleDropdownOptionBuilder.populateNamedDropdown = (el, namedItems, emptyOptionLabel) => {
      captured = { el, namedItems, emptyOptionLabel };
   };

   try {
      ConsoleDropdownPopulator.populateExhibitDropdown(selectEl, items);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.namedItems, items);
      assert.equal(captured.emptyOptionLabel, Strings.placeholders.exhibit);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});


test('Test_PopulateRestaurantDropdown_TestEntities_ExpectPlaceholder', () => {
   const name = 'Cafe';
   const items = [{ name }];
   const selectEl = _select();
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   let captured;
   ConsoleDropdownOptionBuilder.populateNamedDropdown = (el, namedItems, emptyOptionLabel) => {
      captured = { el, namedItems, emptyOptionLabel };
   };

   try {
      ConsoleDropdownPopulator.populateRestaurantDropdown(selectEl, items);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.namedItems, items);
      assert.equal(captured.emptyOptionLabel, Strings.placeholders.restaurant);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});


test('Test_PopulateRestroomDropdown_TestEntities_ExpectPlaceholder', () => {
   const name = 'Main';
   const items = [{ name }];
   const selectEl = _select();
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   let captured;
   ConsoleDropdownOptionBuilder.populateNamedDropdown = (el, namedItems, emptyOptionLabel) => {
      captured = { el, namedItems, emptyOptionLabel };
   };

   try {
      ConsoleDropdownPopulator.populateRestroomDropdown(selectEl, items);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.namedItems, items);
      assert.equal(captured.emptyOptionLabel, Strings.placeholders.restroom);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});


test('Test_PopulateGiftShopDropdown_TestEntities_ExpectPlaceholder', () => {
   const name = 'Shop';
   const items = [{ name }];
   const selectEl = _select();
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   let captured;
   ConsoleDropdownOptionBuilder.populateNamedDropdown = (el, namedItems, emptyOptionLabel) => {
      captured = { el, namedItems, emptyOptionLabel };
   };

   try {
      ConsoleDropdownPopulator.populateGiftShopDropdown(selectEl, items);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.namedItems, items);
      assert.equal(captured.emptyOptionLabel, Strings.placeholders.giftShop);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});


test('Test_PopulateAttractionDropdown_TestEntities_ExpectPlaceholder', () => {
   const name = 'Carousel';
   const items = [{ name }];
   const selectEl = _select();
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   let captured;
   ConsoleDropdownOptionBuilder.populateNamedDropdown = (el, namedItems, emptyOptionLabel) => {
      captured = { el, namedItems, emptyOptionLabel };
   };

   try {
      ConsoleDropdownPopulator.populateAttractionDropdown(selectEl, items);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.namedItems, items);
      assert.equal(captured.emptyOptionLabel, Strings.placeholders.attraction);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});


test('Test_PopulateTransportationStationDropdown_TestEntities_ExpectPlaceholder', () => {
   const name = 'Station';
   const items = [{ name }];
   const selectEl = _select();
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   let captured;
   ConsoleDropdownOptionBuilder.populateNamedDropdown = (el, namedItems, emptyOptionLabel) => {
      captured = { el, namedItems, emptyOptionLabel };
   };

   try {
      ConsoleDropdownPopulator.populateTransportationStationDropdown(selectEl, items);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.namedItems, items);
      assert.equal(captured.emptyOptionLabel, Strings.placeholders.transportationStation);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});


test('Test_PopulateGuardiansTalkDropdown_TestEntities_ExpectPlaceholder', () => {
   const name = 'Talk';
   const items = [{ name }];
   const selectEl = _select();
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   let captured;
   ConsoleDropdownOptionBuilder.populateNamedDropdown = (el, namedItems, emptyOptionLabel) => {
      captured = { el, namedItems, emptyOptionLabel };
   };

   try {
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown(selectEl, items);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.namedItems, items);
      assert.equal(captured.emptyOptionLabel, Strings.placeholders.talk);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});


test('Test_PopulateWildEncounterDropdown_TestEntities_ExpectPlaceholder', () => {
   const name = 'Encounter';
   const items = [{ name }];
   const selectEl = _select();
   const original = ConsoleDropdownOptionBuilder.populateNamedDropdown;
   let captured;
   ConsoleDropdownOptionBuilder.populateNamedDropdown = (el, namedItems, emptyOptionLabel) => {
      captured = { el, namedItems, emptyOptionLabel };
   };

   try {
      ConsoleDropdownPopulator.populateWildEncounterDropdown(selectEl, items);

      assert.equal(captured.el, selectEl);
      assert.deepEqual(captured.namedItems, items);
      assert.equal(captured.emptyOptionLabel, Strings.placeholders.wildEncounter);
   } finally {
      ConsoleDropdownOptionBuilder.populateNamedDropdown = original;
   }
});

import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreFilter } from '../../../scripts/search/exploreFilter.js';
import { Strings } from '../../../scripts/strings.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _createCheckboxOption({ value, label, checked = false }) {
   const labelEl = createDomNode('label');
   const checkbox = createDomNode('input');
   const labelText = createDomNode('#text', '', label);

   checkbox.type = 'checkbox';
   checkbox.value = value;
   checkbox.checked = checked;
   labelEl.appendChild(labelText);
   labelEl.appendChild(checkbox);
   checkbox.closest = (selector) => (
      selector === 'label' ? labelEl : null
   );
   checkbox.dispatchChange = () => {
      checkbox.listeners.change?.();
   };

   return { checkbox, labelEl };
}


function _createExploreTypeFilterDom({
   selected = [],
} = {}) {
   const multiSelect = createDomNode('div', 'multi-select');
   const button = createDomNode('button', 'multi-select-button');
   const dropdown = createDomNode('div', 'multi-select-dropdown');
   const chipContainer = createDomNode('div', 'selected-values');
   const options = [
      { value: ItemType.ANIMAL, label: 'Animals' },
      { value: ItemType.RESTAURANT, label: 'Restaurants' },
   ];
   const checkboxes = options.map((option) => {
      const { checkbox, labelEl } = _createCheckboxOption({
         value: option.value,
         label: option.label,
         checked: selected.includes(option.value),
      });

      dropdown.appendChild(labelEl);

      return checkbox;
   });

   dropdown.querySelectorAll = (selector) => (
      selector === 'input[type="checkbox"]' ? checkboxes : []
   );
   multiSelect.appendChild(button);
   multiSelect.appendChild(dropdown);
   multiSelect.appendChild(chipContainer);
   multiSelect.classList.toggle = (className, shouldAdd) => {
      if (shouldAdd === undefined) {
         if (multiSelect.classList.contains(className)) {
            multiSelect.classList.remove(className);
         }
         else {
            multiSelect.classList.add(className);
         }
         return;
      }

      if (shouldAdd) {
         multiSelect.classList.add(className);
      }
      else {
         multiSelect.classList.remove(className);
      }
   };

   return {
      multiSelect,
      button,
      dropdown,
      chipContainer,
      checkboxes,
   };
}

installDomTestHooks();


function _animalOnlyFlags(overrides = {}) {
   return {
      includeAnimals: true,
      includePavilions: false,
      includeRestaurants: false,
      includeRestrooms: false,
      includeGiftShops: false,
      includeAttractions: false,
      includeGuardiansTalks: false,
      includeWildEncounters: false,
      includeTransportationStations: false,
      ...overrides,
   };
}


test('Test_BuildExploreSearchIncludeFlags_TestSelectedTypes_ExpectSearchFlags', () => {
   const flags = ExploreFilter.buildExploreSearchIncludeFlags(
      [ItemType.ANIMAL, ItemType.RESTAURANT, ItemType.WILD_ENCOUNTER],
      'none'
   );

   assert.deepEqual(flags, _animalOnlyFlags({
      includeRestaurants: true,
      includeWildEncounters: true,
   }));
});


test('Test_BuildExploreSearchIncludeFlags_TestRouteSelected_ExpectStations', () => {
   const transportationRoute = 'current';

   const flags = ExploreFilter.buildExploreSearchIncludeFlags([ItemType.ANIMAL], transportationRoute);

   assert.deepEqual(flags, _animalOnlyFlags({
      includeTransportationStations: true,
      transportationRoute,
   }));
});


test('Test_InitExploreTypeFilter_TestMissingFilter_ExpectFallback', () => {
   const filter = ExploreFilter.initExploreTypeFilter({
      multiSelect: null,
   });

   assert.deepEqual(filter.getSelectedTypes(), [ItemType.ANIMAL]);
   assert.deepEqual(filter.buildSearchIncludeFlags(), _animalOnlyFlags());
});


test('Test_InitExploreTypeFilter_TestRouteSelected_ExpectAnimalsAndRoute', () => {
   const { multiSelect, chipContainer } = _createExploreTypeFilterDom({
      selected: [ItemType.ANIMAL],
   });
   const transportationRoute = 'current';

   const filter = ExploreFilter.initExploreTypeFilter({
      multiSelect,
      getTransportationRoute: () => transportationRoute,
   });

   assert.deepEqual(filter.getSelectedTypes(), [ItemType.ANIMAL, ItemType.TRANSPORTATION_ROUTE]);
   assert.deepEqual(filter.buildSearchIncludeFlags(), _animalOnlyFlags({
      includeTransportationStations: true,
      transportationRoute,
   }));
   assert.equal(chipContainer.children.length, Position.SECOND);
   assert.equal(chipContainer.children.at(Position.FIRST).className, 'filter-chip');
   assert.equal(chipContainer.children.at(Position.FIRST).textContent, 'Animals');
});


test('Test_InitExploreTypeFilter_TestUncheckAnimals_ExpectNoneChip', () => {
   const changeCalls = [];
   const animalsUncheckedCalls = [];
   const { multiSelect, checkboxes, chipContainer } = _createExploreTypeFilterDom({
      selected: [ItemType.ANIMAL],
   });
   const filter = ExploreFilter.initExploreTypeFilter({
      multiSelect,
      getTransportationRoute: () => 'current',
      onChange: () => {
         changeCalls.push('changed');
      },
      onAnimalsUnchecked: () => {
         animalsUncheckedCalls.push('unchecked');
      },
   });

   checkboxes.at(Position.FIRST).checked = false;
   checkboxes.at(Position.FIRST).dispatchChange();

   assert.deepEqual(filter.getSelectedTypes(), [ItemType.TRANSPORTATION_ROUTE]);
   assert.deepEqual(changeCalls, ['changed']);
   assert.deepEqual(animalsUncheckedCalls, ['unchecked']);
   assert.equal(chipContainer.children.at(Position.FIRST).className, 'filter-none');
   assert.equal(
      chipContainer.children.at(Position.FIRST).textContent,
      Strings.map.transportationRoute.none
   );
});


test('Test_InitExploreTypeFilter_TestCheckRestaurant_ExpectRestaurantChip', () => {
   const changeCalls = [];
   const { multiSelect, checkboxes, chipContainer } = _createExploreTypeFilterDom({
      selected: [ItemType.ANIMAL],
   });
   const filter = ExploreFilter.initExploreTypeFilter({
      multiSelect,
      getTransportationRoute: () => 'current',
      onChange: () => {
         changeCalls.push('changed');
      },
   });
   checkboxes.at(Position.FIRST).checked = false;
   checkboxes.at(Position.FIRST).dispatchChange();

   checkboxes.at(Position.SECOND).checked = true;
   checkboxes.at(Position.SECOND).dispatchChange();

   assert.deepEqual(filter.getSelectedTypes(), [ItemType.RESTAURANT, ItemType.TRANSPORTATION_ROUTE]);
   assert.equal(changeCalls.length, 2);
   assert.equal(chipContainer.children.at(Position.FIRST).textContent, 'Restaurants');
});


test('Test_InitExploreTypeFilter_TestDropdownToggle_ExpectOpenClose', () => {
   const documentListeners = {};
   const originalAddEventListener = document.addEventListener;
   document.addEventListener = (eventName, handler) => {
      documentListeners[eventName] = handler;
      originalAddEventListener(eventName, handler);
   };
   const { multiSelect, button } = _createExploreTypeFilterDom({
      selected: [ItemType.ANIMAL],
   });

   try {
      ExploreFilter.initExploreTypeFilter({
         multiSelect,
         getTransportationRoute: () => 'none',
      });
      button.listeners.click?.({
         stopPropagation() {},
      });
      const opened = multiSelect.classList.contains('open');
      documentListeners.click?.();
      const closed = multiSelect.classList.contains('open');

      assert.equal(opened, true);
      assert.equal(closed, false);
   } finally {
      document.addEventListener = originalAddEventListener;
   }
});

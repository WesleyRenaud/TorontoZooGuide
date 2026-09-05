import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreFilter } from '../../../scripts/search/exploreFilter.js';
import { APP_STRINGS } from '../../../scripts/strings.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

function createCheckboxOption({ value, label, checked = false }) {
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

function createExploreTypeFilterDom({
   selected = [],
} = {}) {
   const multiSelect = createDomNode('div', 'multi-select');
   const button = createDomNode('button', 'multi-select-button');
   const dropdown = createDomNode('div', 'multi-select-dropdown');
   const chipContainer = createDomNode('div', 'selected-values');
   const options = [
      { value: 'animal', label: 'Animals' },
      { value: 'restaurant', label: 'Restaurants' },
   ];
   const checkboxes = options.map((option) => {
      const { checkbox, labelEl } = createCheckboxOption({
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

test('Test_BuildExploreSearchIncludeFlags_TestSelectedTypes_ExpectSearchFlags', () => {
   assert.deepEqual(
      ExploreFilter.buildExploreSearchIncludeFlags(
         ['animal', 'restaurant', 'wildEncounter'],
         'none'
      ),
      {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: true,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: true,
         includeTransportationStations: false,
      }
   );
});

test('Test_BuildExploreSearchIncludeFlags_TestRouteSelected_ExpectStations', () => {
   assert.deepEqual(
      ExploreFilter.buildExploreSearchIncludeFlags(['animal'], 'current'),
      {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: false,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: false,
         includeTransportationStations: true,
         transportationRoute: 'current',
      }
   );
});

test.describe('initExploreTypeFilter DOM integration', () => {
   installDomTestHooks();

   test('Test_InitExploreTypeFilter_TestMissingFilter_ExpectFallback', () => {
      const filter = ExploreFilter.initExploreTypeFilter({
         multiSelect: null,
      });

      assert.deepEqual(filter.getSelectedTypes(), ['animal']);
      assert.deepEqual(filter.buildSearchIncludeFlags(), {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: false,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: false,
         includeTransportationStations: false,
      });
   });

   test('Test_InitExploreTypeFilter_TestCheckboxAndRoute_ExpectSelection', () => {
      const changeCalls = [];
      const animalsUncheckedCalls = [];
      const { multiSelect, checkboxes, chipContainer } = createExploreTypeFilterDom({
         selected: ['animal'],
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

      assert.deepEqual(filter.getSelectedTypes(), ['animal', 'transportationRoute']);
      assert.deepEqual(filter.buildSearchIncludeFlags(), {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: false,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: false,
         includeTransportationStations: true,
         transportationRoute: 'current',
      });
      assert.equal(chipContainer.children.length, 1);
      assert.equal(chipContainer.children[0].className, 'filter-chip');
      assert.equal(chipContainer.children[0].textContent, 'Animals');

      checkboxes[0].checked = false;
      checkboxes[0].dispatchChange();

      assert.deepEqual(filter.getSelectedTypes(), ['transportationRoute']);
      assert.deepEqual(changeCalls, ['changed']);
      assert.deepEqual(animalsUncheckedCalls, ['unchecked']);
      assert.equal(chipContainer.children[0].className, 'filter-none');
      assert.equal(
         chipContainer.children[0].textContent,
         APP_STRINGS.map.transportationRoute.none
      );

      checkboxes[1].checked = true;
      checkboxes[1].dispatchChange();

      assert.deepEqual(filter.getSelectedTypes(), ['restaurant', 'transportationRoute']);
      assert.deepEqual(changeCalls, ['changed', 'changed']);
      assert.equal(chipContainer.children[0].textContent, 'Restaurants');
   });

   test('Test_InitExploreTypeFilter_TestDropdownToggle_ExpectOpenClose', () => {
      const documentListeners = {};
      const originalAddEventListener = document.addEventListener;

      document.addEventListener = (eventName, handler) => {
         documentListeners[eventName] = handler;
         originalAddEventListener(eventName, handler);
      };

      const { multiSelect, button } = createExploreTypeFilterDom({
         selected: ['animal'],
      });

      ExploreFilter.initExploreTypeFilter({
         multiSelect,
         getTransportationRoute: () => 'none',
      });

      assert.equal(multiSelect.classList.contains('open'), false);

      button.listeners.click?.({
         stopPropagation() {},
      });
      assert.equal(multiSelect.classList.contains('open'), true);

      documentListeners.click?.();
      assert.equal(multiSelect.classList.contains('open'), false);
   });
});

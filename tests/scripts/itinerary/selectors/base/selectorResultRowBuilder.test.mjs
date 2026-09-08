import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorResultRowBuilder } from '../../../../../scripts/itinerary/selectors/base/selectorResultRowBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateSelectorInfoLink_TestMissingAndPresent_ExpectNullOrAnchor', () => {
   assert.equal(SelectorResultRowBuilder.createSelectorInfoLink(''), null);

   const linkEl = SelectorResultRowBuilder.createSelectorInfoLink('https://example.com');
   assert.equal(linkEl.tagName, 'a');
   assert.equal(linkEl.href, 'https://example.com');
   assert.equal(linkEl.target, '_blank');
   assert.equal(linkEl.textContent, Strings.common.moreInfo);

   const event = { stopPropagation() { event.stopped = true; }, stopped: false };
   linkEl.listeners.click(event);
   assert.equal(event.stopped, true);
});

test('Test_CreateEmptyState_TestText_ExpectEmptyNode', () => {
   const empty = SelectorResultRowBuilder.createEmptyState('Nothing here');
   assert.equal(empty.className, 'itin-empty');
   assert.equal(empty.textContent, 'Nothing here');
});

test('Test_HasRows_TestValues_ExpectBoolean', () => {
   assert.equal(SelectorResultRowBuilder.hasRows([]), false);
   assert.equal(SelectorResultRowBuilder.hasRows([{ id: 1 }]), true);
   assert.equal(SelectorResultRowBuilder.hasRows(null), false);
});

test('Test_CreateToggleButton_TestAddRemove_ExpectToggle', () => {
   const selected = new Set();
   const toggles = [];
   const button = SelectorResultRowBuilder.createToggleButton({
      id: 'lion',
      row: { species: 'Lion' },
      isSelected: (id) => selected.has(id),
      onToggle: (row) => {
         toggles.push(row);
         if (selected.has('lion')) selected.delete('lion');
         else selected.add('lion');
      },
   });

   assert.equal(button.textContent, Strings.itinerary.actions.addSymbol);
   button.listeners.click({ stopPropagation() {} });
   assert.deepEqual(toggles, [{ species: 'Lion' }]);
   assert.equal(button.textContent, Strings.itinerary.actions.remove);
   assert.equal(button.getAttribute('aria-pressed'), 'true');
});

test('Test_CreateResultRowsFragment_TestRows_ExpectFragmentChildren', () => {
   const fragment = SelectorResultRowBuilder.createResultRowsFragment({
      rows: [{ id: 'a' }, { id: 'b' }],
      getId: (row) => row.id,
      isSelected: () => false,
      renderRowLeft: (row) => {
         const el = document.createElement('div');
         el.className = 'left';
         el.textContent = row.id;
         return el;
      },
      onToggle: () => {},
   });

   assert.equal(fragment.children.length, 2);
   assert.equal(fragment.children[0].className, 'animal-result');
});

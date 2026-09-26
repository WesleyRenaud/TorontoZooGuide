import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorResultRowBuilder } from '../../../../../scripts/itinerary/selectors/base/selectorResultRowBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateSelectorInfoLink_TestEmpty_ExpectNull', () => {
   const href = '';

   const linkEl = SelectorResultRowBuilder.createSelectorInfoLink(href);

   assert.equal(linkEl, null);
});


test('Test_CreateSelectorInfoLink_TestPresent_ExpectAnchor', () => {
   const href = 'https://example.com';

   const linkEl = SelectorResultRowBuilder.createSelectorInfoLink(href);

   assert.equal(linkEl.tagName, 'a');
   assert.equal(linkEl.href, href);
   assert.equal(linkEl.target, '_blank');
   assert.equal(linkEl.textContent, Strings.common.moreInfo);
});


test('Test_CreateSelectorInfoLink_TestClick_ExpectStopPropagation', () => {
   const href = 'https://example.com';
   const linkEl = SelectorResultRowBuilder.createSelectorInfoLink(href);
   const event = { stopPropagation() { event.stopped = true; }, stopped: false };

   linkEl.listeners.click(event);

   assert.equal(event.stopped, true);
});


test('Test_CreateEmptyState_TestText_ExpectEmptyNode', () => {
   const text = 'Nothing here';

   const empty = SelectorResultRowBuilder.createEmptyState(text);

   assert.equal(empty.className, 'itin-empty');
   assert.equal(empty.textContent, text);
});


test('Test_HasRows_TestEmpty_ExpectFalse', () => {
   const rows = [];

   const hasRows = SelectorResultRowBuilder.hasRows(rows);

   assert.equal(hasRows, false);
});


test('Test_HasRows_TestPresent_ExpectTrue', () => {
   const rows = [{ id: 1 }];

   const hasRows = SelectorResultRowBuilder.hasRows(rows);

   assert.equal(hasRows, true);
});


test('Test_HasRows_TestNull_ExpectFalse', () => {
   const rows = null;

   const hasRows = SelectorResultRowBuilder.hasRows(rows);

   assert.equal(hasRows, false);
});


test('Test_CreateToggleButton_TestAdd_ExpectAddSymbol', () => {
   const selected = new Set();
   const id = 'lion';
   const row = { species: 'Lion' };
   const button = SelectorResultRowBuilder.createToggleButton({
      id,
      row,
      isSelected: (value) => selected.has(value),
      onToggle: () => {},
   });

   assert.equal(button.textContent, Strings.itinerary.actions.addSymbol);
});


test('Test_CreateToggleButton_TestClick_ExpectToggle', () => {
   const selected = new Set();
   const toggles = [];
   const id = 'lion';
   const row = { species: 'Lion' };
   const button = SelectorResultRowBuilder.createToggleButton({
      id,
      row,
      isSelected: (value) => selected.has(value),
      onToggle: (value) => {
         toggles.push(value);
         if (selected.has(id)) selected.delete(id);
         else selected.add(id);
      },
   });

   button.listeners.click({ stopPropagation() {} });

   assert.deepEqual(toggles, [row]);
   assert.equal(button.textContent, Strings.itinerary.actions.remove);
   assert.equal(button.getAttribute('aria-pressed'), 'true');
});


test('Test_CreateResultRowsFragment_TestRows_ExpectFragmentChildren', () => {
   const firstId = 'a';
   const secondId = 'b';
   const rows = [{ id: firstId }, { id: secondId }];

   const fragment = SelectorResultRowBuilder.createResultRowsFragment({
      rows,
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

   assert.equal(fragment.children.length, rows.length);
   assert.equal(fragment.children.at(Position.FIRST).className, 'animal-result');
});

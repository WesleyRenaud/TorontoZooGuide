import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupContentBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupContentBuilder.js';
import { RemovedItemsPopupKeepButtonStore } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupKeepButtonStore.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_AddAlternativesButton_TestClick_ExpectCallback', () => {
   const calls = [];
   const button = RemovedItemsPopupContentBuilder.addAlternativesButton(
      document.createElement('div'),
      'animals',
      (stepKey) => calls.push(stepKey),
      () => calls.push('removed')
   );

   assert.equal(button.type, 'button');
   assert.equal(button.textContent, Strings.itinerary.removedItems.viewAlternatives);
   button.click();
   assert.deepEqual(calls, ['removed', 'animals']);
   assert.equal(
      RemovedItemsPopupContentBuilder.addAlternativesButton(null, 'animals', () => {}, () => {}),
      null
   );
});

test('Test_AddKeepOverrideButton_TestToggle_ExpectSynced', () => {
   const toggles = [];
   let selected = false;
   const originalApply = RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState;
   const originalGet = RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState;
   const applies = [];

   RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState = (isSelected) => ({
      selected: isSelected,
      textContent: isSelected ? 'remove' : 'keep',
   });
   RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState = (btn, state) => {
      applies.push(state);
      btn.textContent = state.textContent;
   };

   try {
      assert.equal(
         RemovedItemsPopupContentBuilder.addKeepOverrideButton(null, () => 'k', () => {}, () => false),
         null
      );
      assert.equal(
         RemovedItemsPopupContentBuilder.addKeepOverrideButton({}, () => '', () => {}, () => false),
         null
      );

      const button = RemovedItemsPopupContentBuilder.addKeepOverrideButton(
         { species: 'Lion' },
         (item) => item.species,
         (item) => {
            toggles.push(item.species);
            selected = !selected;
         },
         () => selected
      );

      assert.equal(applies[0].textContent, 'keep');
      button.click();
      assert.deepEqual(toggles, ['Lion']);
      assert.equal(applies.at(-1).textContent, 'remove');
   } finally {
      RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState = originalApply;
      RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState = originalGet;
   }
});

test('Test_MakeSection_TestRows_ExpectSectionOrNull', () => {
   assert.equal(RemovedItemsPopupContentBuilder.makeSection('Title', 'Sub', []), null);

   const row = document.createElement('div');
   row.textContent = 'row';
   const section = RemovedItemsPopupContentBuilder.makeSection('Title', 'Sub', [row, null]);

   assert.ok(section.classList.contains('itin-removed-section'));
   assert.match(section.textContent, /Title/);
   assert.match(section.textContent, /Sub/);
   assert.match(section.textContent, /row/);
});

test('Test_BuildSectionRows_TestActions_ExpectButtons', () => {
   const row = document.createElement('div');
   const items = [{ species: 'Lion' }];

   const rows = RemovedItemsPopupContentBuilder.buildSectionRows(
      items,
      () => [row],
      'animals',
      () => {},
      () => {},
      true,
      {
         buildKey: (item) => item.species,
         onToggle: () => {},
         isSelected: () => false,
      }
   );

   assert.equal(rows.length, 1);
   assert.ok(rows[0].classList.contains('itin-removed-row'));
   const actions = rows[0].children.find((child) => (
      child.classList?.contains('itin-removed-row-actions')
   ));
   assert.ok(actions);
   assert.equal(actions.children.length, 2);

   const plain = RemovedItemsPopupContentBuilder.buildSectionRows(
      items,
      () => [document.createElement('div')],
      'animals',
      () => {},
      () => {},
      false,
      null
   );
   assert.equal(plain[0].classList.contains('itin-removed-row'), false);
});

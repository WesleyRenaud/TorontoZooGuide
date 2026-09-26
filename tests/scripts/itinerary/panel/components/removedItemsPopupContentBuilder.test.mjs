import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupContentBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupContentBuilder.js';
import { RemovedItemsPopupKeepButtonStore } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupKeepButtonStore.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_AddAlternativesButton_TestClick_ExpectCallback', () => {
   const stepKey = 'animals';
   const removedLabel = 'removed';
   const calls = [];

   const button = RemovedItemsPopupContentBuilder.addAlternativesButton(
      document.createElement('div'),
      stepKey,
      (clickedStep) => calls.push(clickedStep),
      () => calls.push(removedLabel)
   );
   button.click();

   assert.equal(button.type, 'button');
   assert.equal(button.textContent, Strings.itinerary.removedItems.viewAlternatives);
   assert.deepEqual(calls, [removedLabel, stepKey]);
});


test('Test_AddAlternativesButton_TestNullRow_ExpectNull', () => {
   const button = RemovedItemsPopupContentBuilder.addAlternativesButton(
      null,
      'animals',
      () => {},
      () => {}
   );

   assert.equal(button, null);
});


test('Test_AddKeepOverrideButton_TestNullItem_ExpectNull', () => {
   const button = RemovedItemsPopupContentBuilder.addKeepOverrideButton(
      null,
      () => 'k',
      () => {},
      () => false
   );

   assert.equal(button, null);
});


test('Test_AddKeepOverrideButton_TestEmptyKey_ExpectNull', () => {
   const button = RemovedItemsPopupContentBuilder.addKeepOverrideButton(
      {},
      () => '',
      () => {},
      () => false
   );

   assert.equal(button, null);
});


test('Test_AddKeepOverrideButton_TestToggle_ExpectSynced', () => {
   const originalApply = RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState;
   const originalGet = RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState;
   const species = 'African Lion';
   const keepLabel = 'keep';
   const removeLabel = 'remove';
   const toggles = [];
   const applies = [];
   let selected = false;

   RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState = (isSelected) => ({
      selected: isSelected,
      textContent: isSelected ? removeLabel : keepLabel,
   });
   RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState = (btn, state) => {
      applies.push(state);
      btn.textContent = state.textContent;
   };

   try {
      const button = RemovedItemsPopupContentBuilder.addKeepOverrideButton(
         { species },
         (item) => item.species,
         (item) => {
            toggles.push(item.species);
            selected = !selected;
         },
         () => selected
      );
      button.click();

      assert.equal(applies.at(Position.FIRST).textContent, keepLabel);
      assert.deepEqual(toggles, [species]);
      assert.equal(applies.at(Position.LAST).textContent, removeLabel);
   } finally {
      RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState = originalApply;
      RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState = originalGet;
   }
});


test('Test_MakeSection_TestEmptyRows_ExpectNull', () => {
   const title = 'Removed animals';
   const subtitle = 'These animals left the itinerary';

   const section = RemovedItemsPopupContentBuilder.makeSection(title, subtitle, []);

   assert.equal(section, null);
});


test('Test_MakeSection_TestRows_ExpectSection', () => {
   const title = 'Removed animals';
   const subtitle = 'These animals left the itinerary';
   const rowText = 'African Lion';
   const row = document.createElement('div');
   row.textContent = rowText;

   const section = RemovedItemsPopupContentBuilder.makeSection(title, subtitle, [row, null]);

   assert.ok(section.classList.contains('itin-removed-section'));
   assert.match(section.textContent, new RegExp(title));
   assert.match(section.textContent, new RegExp(subtitle));
   assert.match(section.textContent, new RegExp(rowText));
});


test('Test_BuildSectionRows_TestActions_ExpectButtons', () => {
   const species = 'African Lion';
   const items = [{ species }];
   const row = document.createElement('div');

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
   const actions = rows.at(Position.FIRST).children.find((child) => (
      child.classList?.contains('itin-removed-row-actions')
   ));

   assert.equal(rows.length, items.length);
   assert.ok(rows.at(Position.FIRST).classList.contains('itin-removed-row'));
   assert.ok(actions);
   assert.equal(actions.children.length, 2);
});


test('Test_BuildSectionRows_TestWithoutActions_ExpectPlainRow', () => {
   const items = [{ species: 'African Lion' }];

   const rows = RemovedItemsPopupContentBuilder.buildSectionRows(
      items,
      () => [document.createElement('div')],
      'animals',
      () => {},
      () => {},
      false,
      null
   );

   assert.equal(rows.at(Position.FIRST).classList.contains('itin-removed-row'), false);
});

import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelViewsHelper } from '../../../../../scripts/itinerary/panel/components/itineraryPanelViewsHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_MakeToggleButton_TestActive_ExpectPressed', () => {
   let selected = null;
   const button = ItineraryPanelViewsHelper.makeToggleButton({
      label: 'Day',
      view: 'day',
      activeView: 'day',
      onSelect: (view) => { selected = view; },
   });

   assert.equal(button.dataset.view, 'day');
   assert.equal(button.getAttribute('aria-pressed'), 'true');
   button.click();
   assert.equal(selected, 'day');
});

test('Test_SetViewVisibility_TestSelectedView_ExpectActiveAndHidden', () => {
   const root = document.createElement('div');
   const buttonA = document.createElement('button');
   buttonA.className = 'itin-panel-view-toggle-button';
   buttonA.dataset.view = 'a';
   const buttonB = document.createElement('button');
   buttonB.className = 'itin-panel-view-toggle-button';
   buttonB.dataset.view = 'b';
   const viewA = document.createElement('div');
   viewA.className = 'itin-panel-view';
   viewA.dataset.view = 'a';
   const viewB = document.createElement('div');
   viewB.className = 'itin-panel-view';
   viewB.dataset.view = 'b';
   root.append(buttonA, buttonB, viewA, viewB);

   ItineraryPanelViewsHelper.setViewVisibility(root, 'b');

   assert.equal(buttonB.classList.contains('itin-panel-view-toggle-button-active'), true);
   assert.equal(buttonA.getAttribute('aria-pressed'), 'false');
   assert.equal(viewA.hidden, true);
   assert.equal(viewB.hidden, false);
});

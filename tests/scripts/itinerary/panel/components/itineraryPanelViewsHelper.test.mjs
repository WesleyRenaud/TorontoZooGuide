import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelViewsHelper } from '../../../../../scripts/itinerary/panel/components/itineraryPanelViewsHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_MakeToggleButton_TestActive_ExpectPressed', () => {
   const view = 'day';
   let selected = null;

   const button = ItineraryPanelViewsHelper.makeToggleButton({
      label: 'Day',
      view,
      activeView: view,
      onSelect: (selectedView) => {
         selected = selectedView;
      },
   });

   assert.equal(button.dataset.view, view);
   assert.equal(button.getAttribute('aria-pressed'), 'true');
   button.click();
   assert.equal(selected, view);
});


test('Test_SetViewVisibility_TestSelectedView_ExpectActiveAndHidden', () => {
   const listViewName = 'list';
   const dayPlannerViewName = 'dayPlanner';
   const root = document.createElement('div');
   const listButton = document.createElement('button');
   listButton.className = 'itin-panel-view-toggle-button';
   listButton.dataset.view = listViewName;
   const dayPlannerButton = document.createElement('button');
   dayPlannerButton.className = 'itin-panel-view-toggle-button';
   dayPlannerButton.dataset.view = dayPlannerViewName;
   const listView = document.createElement('div');
   listView.className = 'itin-panel-view';
   listView.dataset.view = listViewName;
   const dayPlannerView = document.createElement('div');
   dayPlannerView.className = 'itin-panel-view';
   dayPlannerView.dataset.view = dayPlannerViewName;
   root.append(listButton, dayPlannerButton, listView, dayPlannerView);

   ItineraryPanelViewsHelper.setViewVisibility(root, dayPlannerViewName);

   assert.equal(
      dayPlannerButton.classList.contains('itin-panel-view-toggle-button-active'),
      true
   );
   assert.equal(listButton.getAttribute('aria-pressed'), 'false');
   assert.equal(listView.hidden, true);
   assert.equal(dayPlannerView.hidden, false);
});

import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySettingsView } from '../../../../scripts/itinerary/settings/itinerarySettingsView.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BuildItinerarySettingsView_TestStatuses_ExpectTallCardAndSave', () => {
   const view = ItinerarySettingsView.buildItinerarySettingsView({
      statuses: [
         {
            status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
            isSuppressable: true,
            isSuppressed: false,
         },
         {
            status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            isSuppressable: true,
            isSuppressed: true,
         },
      ],
   });

   assert.equal(view.root.className, 'itin-overlay itin-settings-overlay');
   assert.equal(view.root.querySelector('.itin-card').className, 'itin-card itin-card-tall');
   assert.equal(
      view.root.querySelector('.itin-h1').textContent,
      Strings.itinerary.settings.heading
   );
   assert.equal(
      view.closeButtonEl.getAttribute('aria-label'),
      Strings.itinerary.settings.closeAriaLabel
   );
   assert.equal(view.saveButtonEl.textContent, Strings.actions.save);
   assert.equal(view.checkboxEls.length, 2);
   assert.equal(view.checkboxEls[Position.FIRST].checked, true);
   assert.equal(view.checkboxEls[Position.SECOND].checked, false);
   assert.equal(
      view.root.querySelector('.itin-settings-row-title').textContent,
      Strings.itinerary.confirmation.shortVisitTitle
   );
});

test('Test_BuildItinerarySettingsView_TestDefaults_ExpectEmptyList', () => {
   const view = ItinerarySettingsView.buildItinerarySettingsView();

   assert.equal(view.checkboxEls.length, 0);
   assert.equal(view.saveButtonEl.textContent, Strings.actions.save);
});

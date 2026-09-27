import assert from 'node:assert/strict';
import { test } from 'node:test';

import { VisitWindowOverflowFragment } from '../../../../scripts/itinerary/panel/visitWindowOverflowFragment.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ItineraryVisitWindowOverflowEnd } from '../../../../scripts/shared/enums/itineraryVisitWindowOverflowEnd.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { cleanupConfirmPopup } from '../../helpers/confirmPopupTestSetup.mjs';


const talkItem = {
   name: 'African Lion',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   start_time: '10:00 AM',
   end_time: '10:30 AM',
   overflow_end: ItineraryVisitWindowOverflowEnd.ARRIVAL,
};

installDomTestHooks({
   after: () => {
      cleanupConfirmPopup();
   },
});


test('Test_ShowVisitWindowOverflowConfirmation_TestDefaults_ExpectPopup', () => {
   const issues = [
      {
         type: ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
         items: [talkItem],
      },
   ];

   VisitWindowOverflowFragment.showVisitWindowOverflowConfirmation({ issues });

   const popup = document.querySelector('.tzg-confirm');
   assert.ok(popup);
   assert.equal(
      popup.querySelector('.itin-top-title').textContent,
      Strings.itinerary.confirmation.visitWindowOverflowTitle
   );
   assert.equal(
      popup.querySelector('.itin-save-issue-conflict-message').textContent,
      Strings.itinerary.confirmation.visitWindowOverflowMessage
   );
});


test('Test_ShowVisitWindowOverflowConfirmation_TestCancel_ExpectCancelled', () => {
   const cancelled = 'cancelled';
   const cancelCalls = [];

   VisitWindowOverflowFragment.showVisitWindowOverflowConfirmation({
      onCancel: () => {
         cancelCalls.push(cancelled);
      },
   });
   const cancelButton = document.querySelector('.tzg-popup-cancel');

   cancelButton.click();

   assert.deepEqual(cancelCalls, [cancelled]);
});


test('Test_ShowVisitWindowOverflowConfirmation_TestConfirm_ExpectKeptItems', () => {
   const confirmCalls = [];
   const issues = [
      {
         type: ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
         items: [talkItem],
      },
   ];

   VisitWindowOverflowFragment.showVisitWindowOverflowConfirmation({
      issues,
      onConfirm: (confirmArg) => {
         confirmCalls.push(confirmArg);
      },
   });
   const confirmButton = document.querySelector('.tzg-popup-confirm');

   confirmButton.click();

   assert.deepEqual(confirmCalls[Position.FIRST].keptVisitWindowOverflowItems, [
      {
         name: talkItem.name,
         item_type: talkItem.item_type,
         start_time: talkItem.start_time,
      },
   ]);
});

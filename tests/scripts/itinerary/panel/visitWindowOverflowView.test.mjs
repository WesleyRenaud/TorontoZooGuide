import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AssetKeyNormalizer } from '../../../../scripts/assets/assetKeyNormalizer.js';
import { VisitWindowOverflowView } from '../../../../scripts/itinerary/panel/visitWindowOverflowView.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ItineraryVisitWindowOverflowEnd } from '../../../../scripts/shared/enums/itineraryVisitWindowOverflowEnd.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';


const talkItem = {
   name: 'African Lion',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   start_time: '10:00 AM',
   end_time: '10:30 AM',
   overflow_end: ItineraryVisitWindowOverflowEnd.ARRIVAL,
};

installDomTestHooks();


test('Test_BuildItemImageSrc_TestTalk_ExpectPath', () => {
   const src = VisitWindowOverflowView.buildItemImageSrc(talkItem);

   assert.equal(
      src,
      `images/details/guardians-talks/${AssetKeyNormalizer.normalize(talkItem.name)}.png`
   );
});


test('Test_CreateContent_TestOverflowItems_ExpectKeptByDefault', () => {
   const issues = [
      {
         type: ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
         items: [talkItem],
      },
   ];

   const { content, getKeptItems } = VisitWindowOverflowView.createContent(issues);

   assert.equal(
      content.querySelector('.itin-save-issue-conflict-message').textContent,
      Strings.itinerary.confirmation.visitWindowOverflowMessage
   );
   assert.match(
      content.textContent,
      new RegExp(Strings.itinerary.confirmation.visitWindowOverflowArrivalEnd)
   );
   assert.deepEqual(getKeptItems(), [
      {
         name: talkItem.name,
         item_type: talkItem.item_type,
         start_time: talkItem.start_time,
      },
   ]);
});


test('Test_CreateContent_TestToggleKeep_ExpectDropped', () => {
   const issues = [
      {
         type: ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
         items: [talkItem],
      },
   ];
   const { content, getKeptItems } = VisitWindowOverflowView.createContent(issues);
   const button = content.querySelector('.itin-save-issue-select-btn');

   button.click();

   assert.deepEqual(getKeptItems(), []);
   assert.equal(button.textContent, Strings.itinerary.actions.addSymbol);
});


test('Test_OverflowEndLabel_TestBoth_ExpectBothCopy', () => {
   const item = {
      overflow_end: ItineraryVisitWindowOverflowEnd.BOTH,
   };

   const label = VisitWindowOverflowView.overflowEndLabel(item);

   assert.equal(label, Strings.itinerary.confirmation.visitWindowOverflowBothEnds);
});


test('Test_OverflowEndLabel_TestDeparture_ExpectDepartureCopy', () => {
   const item = {
      overflow_end: ItineraryVisitWindowOverflowEnd.DEPARTURE,
   };

   const label = VisitWindowOverflowView.overflowEndLabel(item);

   assert.equal(label, Strings.itinerary.confirmation.visitWindowOverflowDepartureEnd);
});


test('Test_OverflowEndLabel_TestUnknown_ExpectEmpty', () => {
   const item = {};

   const label = VisitWindowOverflowView.overflowEndLabel(item);

   assert.equal(label, '');
});


test('Test_ImageDirectoryForItem_TestAttraction_ExpectAttractions', () => {
   const item = {
      item_type: ItinerarySaveIssueItemType.ATTRACTION,
   };

   const directory = VisitWindowOverflowView.imageDirectoryForItem(item);

   assert.equal(directory, 'attractions');
});


test('Test_ImageDirectoryForItem_TestWildEncounter_ExpectWildEncounters', () => {
   const item = {
      item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   };

   const directory = VisitWindowOverflowView.imageDirectoryForItem(item);

   assert.equal(directory, 'wild-encounters');
});

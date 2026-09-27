import assert from 'node:assert/strict';
import { test } from 'node:test';

import { VisitWindowOverflowKeepItems } from '../../../../scripts/itinerary/panel/visitWindowOverflowKeepItems.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


const TALK_NAME = 'African Lion';
const ATTRACTION_NAME = 'Splash Island';

const talkItem = {
   name: TALK_NAME,
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   start_time: '10:00 AM',
};

const attractionItem = {
   name: ATTRACTION_NAME,
   item_type: ItinerarySaveIssueItemType.ATTRACTION,
   start_time: '12:30 PM',
};


test('Test_OverflowItemsFromIssues_TestOverflowReason_ExpectItems', () => {
   const issues = [
      {
         type: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         items: [attractionItem],
      },
      {
         type: ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
         items: [talkItem, attractionItem],
      },
   ];

   const items = VisitWindowOverflowKeepItems.overflowItemsFromIssues(issues);

   assert.deepEqual(items, [talkItem, attractionItem]);
});


test('Test_CreateKeptItemKeys_TestItems_ExpectAllKept', () => {
   const items = [talkItem, attractionItem];

   const keptItemKeys = VisitWindowOverflowKeepItems.createKeptItemKeys(items);

   assert.equal(VisitWindowOverflowKeepItems.isKept(keptItemKeys, talkItem), true);
   assert.equal(VisitWindowOverflowKeepItems.isKept(keptItemKeys, attractionItem), true);
});


test('Test_ToggleKeep_TestKeptItem_ExpectDropped', () => {
   const keptItemKeys = VisitWindowOverflowKeepItems.createKeptItemKeys([talkItem]);

   VisitWindowOverflowKeepItems.toggleKeep(keptItemKeys, talkItem);

   assert.equal(VisitWindowOverflowKeepItems.isKept(keptItemKeys, talkItem), false);
});


test('Test_ToggleKeep_TestDroppedItem_ExpectKept', () => {
   const keptItemKeys = VisitWindowOverflowKeepItems.createKeptItemKeys([talkItem]);
   VisitWindowOverflowKeepItems.toggleKeep(keptItemKeys, talkItem);

   VisitWindowOverflowKeepItems.toggleKeep(keptItemKeys, talkItem);

   assert.equal(VisitWindowOverflowKeepItems.isKept(keptItemKeys, talkItem), true);
});


test('Test_ToKeepWire_TestAttractionWithoutStart_ExpectNameAndType', () => {
   const item = {
      name: ATTRACTION_NAME,
      item_type: ItinerarySaveIssueItemType.ATTRACTION,
   };

   const keepItem = VisitWindowOverflowKeepItems.toKeepWire(item);

   assert.deepEqual(keepItem, {
      name: item.name,
      item_type: item.item_type,
   });
});


test('Test_ToKeepWire_TestTalk_ExpectSnakeCaseFields', () => {
   const keepItem = VisitWindowOverflowKeepItems.toKeepWire(talkItem);

   assert.deepEqual(keepItem, {
      name: talkItem.name,
      item_type: talkItem.item_type,
      start_time: talkItem.start_time,
   });
});


test('Test_KeptWiresFromKeys_TestDroppedTalk_ExpectAttractionOnly', () => {
   const items = [talkItem, attractionItem];
   const keptItemKeys = VisitWindowOverflowKeepItems.createKeptItemKeys(items);
   VisitWindowOverflowKeepItems.toggleKeep(keptItemKeys, talkItem);

   const keepItems = VisitWindowOverflowKeepItems.keptWiresFromKeys(items, keptItemKeys);

   assert.equal(keepItems.length, 1);
   assert.equal(keepItems[Position.FIRST].name, attractionItem.name);
});

import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterConflictResolutionHelper } from '../../../../scripts/itinerary/wizard/wildEncounterConflictResolutionHelper.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';


test('Test_ToConflictResolutionDraftItem_TestGuardiansTalk_ExpectNameAndLocation', () => {
   const name = 'Lion Talk';
   const location = 'Theatre';
   const item = {
      item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
      name,
      location,
   };

   const draftItem = WildEncounterConflictResolutionHelper.toConflictResolutionDraftItem(item);

   assert.deepEqual(draftItem, { name, location });
});


test('Test_ToConflictResolutionDraftItem_TestWildEncounter_ExpectNameAndMeetingSpot', () => {
   const name = 'Red Panda';
   const meetingSpot = 'Pavilion';
   const item = {
      name,
      meeting_spot: meetingSpot,
   };

   const draftItem = WildEncounterConflictResolutionHelper.toConflictResolutionDraftItem(item);

   assert.deepEqual(draftItem, { name, meeting_spot: meetingSpot });
});


test('Test_GetDraftItemName_TestString_ExpectName', () => {
   const name = 'Carousel';

   const draftName = WildEncounterConflictResolutionHelper.getDraftItemName(name);

   assert.equal(draftName, name);
});


test('Test_GetDraftItemName_TestObject_ExpectName', () => {
   const name = 'Zoomobile';
   const item = { name };

   const draftName = WildEncounterConflictResolutionHelper.getDraftItemName(item);

   assert.equal(draftName, name);
});


test('Test_GetDraftItemName_TestEmptyObject_ExpectEmpty', () => {
   const item = {};

   const draftName = WildEncounterConflictResolutionHelper.getDraftItemName(item);

   assert.equal(draftName, '');
});

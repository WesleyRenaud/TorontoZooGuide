import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
import { WildEncounterConflictResolver } from '../../../../scripts/itinerary/wizard/wildEncounterConflictResolver.js';

const firstEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
};

const secondEncounter = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

const thirdEncounter = {
   name: 'Savanna Safari',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
};

const fourthEncounter = {
   name: 'Guardians of Gorillas',
   start_time: '14:30',
   end_time: '15:00',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
};

const guardiansTalk = {
   name: 'African Lion',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   location: 'Africa Savanna',
};

const _emptyItinerary = {
   date: '2026-06-15',
   animals: [],
   attractions: [],
   guardiansTalks: [],
   wildEncounters: [],
};


test('Test_GetWildEncounterConflictIssueStartTime_TestUsesTheEarliestEncounterTime_ExpectOk', () => {
   const issue = {
      items: [thirdEncounter, fourthEncounter],
   };

   const startTime = WildEncounterConflictResolver.getWildEncounterConflictIssueStartTime(issue);

   assert.equal(startTime, thirdEncounter.start_time);
});


test('Test_SortWildEncounterConflictIssuesByStartTime_TestOrdersGroupsByEarliestTime_ExpectOk', () => {
   const afternoonIssue = {
      items: [thirdEncounter, fourthEncounter],
   };
   const middayIssue = {
      items: [firstEncounter, secondEncounter],
   };

   const sorted = WildEncounterConflictResolver.sortWildEncounterConflictIssuesByStartTime([
      afternoonIssue,
      middayIssue,
   ]);

   assert.deepEqual(sorted, [middayIssue, afternoonIssue]);
});


test('Test_GetSelectedWildEncounters_TestReturnsSelectionsFromEachConflictGroup_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [thirdEncounter] } },
   ];

   const selected = WildEncounterConflictResolver.getSelectedWildEncounters(conflictGroups);

   assert.deepEqual(selected, [firstEncounter, thirdEncounter]);
});


test('Test_GetSelectedWildEncounters_TestReturnsMultipleNonOverlappingPicksInOneGroup_ExpectOk', () => {
   const conflictGroups = [
      {
         selection: {
            items: [firstEncounter, thirdEncounter],
         },
      },
   ];

   const selected = WildEncounterConflictResolver.getSelectedWildEncounters(conflictGroups);

   assert.deepEqual(selected, [firstEncounter, thirdEncounter]);
});


test('Test_GetSelectedWildEncounters_TestDeduplicatesTheSameEncounterSelectedTwice_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [firstEncounter] } },
   ];

   const selected = WildEncounterConflictResolver.getSelectedWildEncounters(conflictGroups);

   assert.deepEqual(selected, [firstEncounter]);
});


test('Test_HasWildEncounterConflictSelection_TestEmpty_ExpectFalse', () => {
   const conflictGroups = [];

   const hasSelection = WildEncounterConflictResolver.hasWildEncounterConflictSelection(conflictGroups);

   assert.equal(hasSelection, false);
});


test('Test_HasWildEncounterConflictSelection_TestIsFalseUntilAGroupHasASelection_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [] } },
      { selection: { items: [thirdEncounter] } },
   ];

   const hasSelection = WildEncounterConflictResolver.hasWildEncounterConflictSelection(conflictGroups);

   assert.equal(hasSelection, true);
});


test('Test_HasUnresolvedWildEncounterConflictGroups_TestEmpty_ExpectFalse', () => {
   const conflictGroups = [];

   const unresolved = WildEncounterConflictResolver.hasUnresolvedWildEncounterConflictGroups(
      conflictGroups
   );

   assert.equal(unresolved, false);
});


test('Test_HasUnresolvedWildEncounterConflictGroups_TestDetectsPartialResolution_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [] } },
   ];

   const unresolved = WildEncounterConflictResolver.hasUnresolvedWildEncounterConflictGroups(
      conflictGroups
   );

   assert.equal(unresolved, true);
});


test('Test_HasUnresolvedWildEncounterConflictGroups_TestAllSelected_ExpectFalse', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [thirdEncounter] } },
   ];

   const unresolved = WildEncounterConflictResolver.hasUnresolvedWildEncounterConflictGroups(
      conflictGroups
   );

   assert.equal(unresolved, false);
});


test('Test_HasUnresolvedWildEncounterConflictGroups_TestAllEmpty_ExpectFalse', () => {
   const conflictGroups = [
      { selection: { items: [] } },
      { selection: { items: [] } },
   ];

   const unresolved = WildEncounterConflictResolver.hasUnresolvedWildEncounterConflictGroups(
      conflictGroups
   );

   assert.equal(unresolved, false);
});


test('Test_IsGuardiansTalkConflictItem_TestTalk_ExpectTrue', () => {
   const isTalk = ScheduleConflictChecker.isGuardiansTalkConflictItem(guardiansTalk);

   assert.equal(isTalk, true);
});


test('Test_IsGuardiansTalkConflictItem_TestEncounter_ExpectFalse', () => {
   const isTalk = ScheduleConflictChecker.isGuardiansTalkConflictItem(firstEncounter);

   assert.equal(isTalk, false);
});


test('Test_GetSelectedGuardiansTalks_TestReturnsOnlyGuardiansTalkSelections_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [guardiansTalk] } },
      { selection: { items: [firstEncounter] } },
   ];

   const talks = WildEncounterConflictResolver.getSelectedGuardiansTalks(conflictGroups);

   assert.deepEqual(talks, [guardiansTalk]);
});


test('Test_BuildItineraryWithSelectedConflictResolutions_TestOmitsScheduleTimesForBackendTrimming_ExpectOk', () => {
   const itinerary = { ..._emptyItinerary };
   const encounterName = 'Grizzly Bear';
   const meetingSpot = 'Spot';
   const talkName = 'African Lion';
   const location = 'Africa Savanna';
   const encounter = {
      name: encounterName,
      start_time: '13:00',
      end_time: '13:45',
      item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
      meeting_spot: meetingSpot,
   };
   const talk = {
      name: talkName,
      start_time: '13:30',
      end_time: '14:00',
      item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
      location,
   };

   const resolved = WildEncounterConflictResolver.buildItineraryWithSelectedConflictResolutions(
      itinerary,
      [encounter, talk]
   );

   assert.deepEqual(resolved, {
      ...itinerary,
      guardiansTalks: [{
         name: talk.name,
         location: talk.location,
      }],
      wildEncounters: [{
         name: encounter.name,
         meeting_spot: encounter.meeting_spot,
      }],
   });
});


test('Test_BuildItineraryWithSelectedConflictResolutions_TestAppendsTalksAndEncounters_ExpectOk', () => {
   const itinerary = { ..._emptyItinerary };

   const resolved = WildEncounterConflictResolver.buildItineraryWithSelectedConflictResolutions(
      itinerary,
      [guardiansTalk, firstEncounter]
   );

   assert.deepEqual(resolved, {
      ...itinerary,
      guardiansTalks: [{
         name: guardiansTalk.name,
         location: guardiansTalk.location,
      }],
      wildEncounters: [{
         name: firstEncounter.name,
         meeting_spot: firstEncounter.meeting_spot,
      }],
   });
});


test('Test_BuildItineraryWithSelectedWildEncounters_TestAppendsAllSelectedEncounters_ExpectOk', () => {
   const itinerary = { ..._emptyItinerary };
   const encounters = [firstEncounter, secondEncounter, thirdEncounter, fourthEncounter];

   const resolved = WildEncounterConflictResolver.buildItineraryWithSelectedWildEncounters(
      itinerary,
      encounters
   );

   assert.deepEqual(resolved, {
      ...itinerary,
      wildEncounters: encounters,
   });
});

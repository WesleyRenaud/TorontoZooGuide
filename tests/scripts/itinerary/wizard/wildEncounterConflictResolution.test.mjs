import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleConflictCompatibility } from '../../../../scripts/itinerary/wizard/scheduleConflictCompatibility.js';
import { WildEncounterConflictResolution } from '../../../../scripts/itinerary/wizard/wildEncounterConflictResolution.js';

const firstEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
};

const secondEncounter = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

const thirdEncounter = {
   name: 'Savanna Safari',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
};

const fourthEncounter = {
   name: 'Guardians of Gorillas',
   start_time: '14:30',
   end_time: '15:00',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
};

const guardiansTalk = {
   name: 'African Lion',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.guardiansTalk,
   location: 'Africa Savanna',
};

test('Test_GetWildEncounterConflictIssueStartTime_TestUsesTheEarliestEncounterTime_ExpectOk', () => {
   assert.equal(
      WildEncounterConflictResolution.getWildEncounterConflictIssueStartTime({
         items: [thirdEncounter, fourthEncounter],
      }),
      '14:00'
   );
});

test('Test_SortWildEncounterConflictIssuesByStartTime_TestOrdersGroupsByEarliestTime_ExpectOk', () => {
   const afternoonIssue = {
      items: [thirdEncounter, fourthEncounter],
   };
   const middayIssue = {
      items: [firstEncounter, secondEncounter],
   };

   assert.deepEqual(
      WildEncounterConflictResolution.sortWildEncounterConflictIssuesByStartTime([
         afternoonIssue,
         middayIssue,
      ]),
      [middayIssue, afternoonIssue]
   );
});

test('Test_GetSelectedWildEncounters_TestReturnsSelectionsFromEachConflictGroup_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [thirdEncounter] } },
   ];

   assert.deepEqual(
      WildEncounterConflictResolution.getSelectedWildEncounters(conflictGroups),
      [firstEncounter, thirdEncounter]
   );
});

test('Test_GetSelectedWildEncounters_TestReturnsMultipleNonOverlappingPicksInOneGroup_ExpectOk', () => {
   const conflictGroups = [
      {
         selection: {
            items: [firstEncounter, thirdEncounter],
         },
      },
   ];

   assert.deepEqual(
      WildEncounterConflictResolution.getSelectedWildEncounters(conflictGroups),
      [firstEncounter, thirdEncounter]
   );
});

test('Test_GetSelectedWildEncounters_TestDeduplicatesTheSameEncounterSelectedTwice_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [firstEncounter] } },
   ];

   assert.deepEqual(
      WildEncounterConflictResolution.getSelectedWildEncounters(conflictGroups),
      [firstEncounter]
   );
});

test('Test_HasWildEncounterConflictSelection_TestIsFalseUntilAGroupHasASelection_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [] } },
      { selection: { items: [thirdEncounter] } },
   ];

   assert.equal(WildEncounterConflictResolution.hasWildEncounterConflictSelection([]), false);
   assert.equal(WildEncounterConflictResolution.hasWildEncounterConflictSelection(conflictGroups), true);
});

test('Test_HasUnresolvedWildEncounterConflictGroups_TestDetectsPartialResolution_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [] } },
   ];

   assert.equal(WildEncounterConflictResolution.hasUnresolvedWildEncounterConflictGroups([]), false);
   assert.equal(
      WildEncounterConflictResolution.hasUnresolvedWildEncounterConflictGroups(conflictGroups),
      true
   );
   assert.equal(
      WildEncounterConflictResolution.hasUnresolvedWildEncounterConflictGroups([
         { selection: { items: [firstEncounter] } },
         { selection: { items: [thirdEncounter] } },
      ]),
      false
   );
   assert.equal(
      WildEncounterConflictResolution.hasUnresolvedWildEncounterConflictGroups([
         { selection: { items: [] } },
         { selection: { items: [] } },
      ]),
      false
   );
});

test('Test_IsGuardiansTalkConflictItem_TestIdentifiesGuardiansTalkIssueItems_ExpectOk', () => {
   assert.equal(
      ScheduleConflictCompatibility.isGuardiansTalkConflictItem(guardiansTalk),
      true
   );
   assert.equal(
      ScheduleConflictCompatibility.isGuardiansTalkConflictItem(firstEncounter),
      false
   );
});

test('Test_GetSelectedGuardiansTalks_TestReturnsOnlyGuardiansTalkSelections_ExpectOk', () => {
   const conflictGroups = [
      { selection: { items: [guardiansTalk] } },
      { selection: { items: [firstEncounter] } },
   ];

   assert.deepEqual(
      WildEncounterConflictResolution.getSelectedGuardiansTalks(conflictGroups),
      [guardiansTalk]
   );
});

test('Test_BuildItineraryWithSelectedConflictResolutions_TestOmitsScheduleTimesForBackendTrimming_ExpectOk', () => {
   const itinerary = {
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };
   const encounter = {
      name: 'Grizzly Bear',
      start_time: '13:00',
      end_time: '13:45',
      item_type: ItinerarySaveIssueItemType.wildEncounter,
      meeting_spot: 'Spot',
   };
   const talk = {
      name: 'African Lion',
      start_time: '13:30',
      end_time: '14:00',
      item_type: ItinerarySaveIssueItemType.guardiansTalk,
      location: 'Africa Savanna',
   };

   assert.deepEqual(
      WildEncounterConflictResolution.buildItineraryWithSelectedConflictResolutions(
         itinerary,
         [encounter, talk]
      ),
      {
         ...itinerary,
         guardiansTalks: [{
            name: 'African Lion',
            location: 'Africa Savanna',
         }],
         wildEncounters: [{
            name: 'Grizzly Bear',
            meeting_spot: 'Spot',
         }],
      }
   );
});

test('Test_BuildItineraryWithSelectedConflictResolutions_TestAppendsTalksAndEncounters_ExpectOk', () => {
   const itinerary = {
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };

   assert.deepEqual(
      WildEncounterConflictResolution.buildItineraryWithSelectedConflictResolutions(
         itinerary,
         [guardiansTalk, firstEncounter]
      ),
      {
         ...itinerary,
         guardiansTalks: [{
            name: guardiansTalk.name,
            location: guardiansTalk.location,
         }],
         wildEncounters: [{
            name: firstEncounter.name,
            meeting_spot: firstEncounter.meeting_spot,
         }],
      }
   );
});

test('Test_BuildItineraryWithSelectedWildEncounters_TestAppendsAllSelectedEncounters_ExpectOk', () => {
   const itinerary = {
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };

   assert.deepEqual(
      WildEncounterConflictResolution.buildItineraryWithSelectedWildEncounters(
         itinerary,
         [firstEncounter, secondEncounter, thirdEncounter, fourthEncounter]
      ),
      {
         ...itinerary,
         wildEncounters: [
            firstEncounter,
            secondEncounter,
            thirdEncounter,
            fourthEncounter,
         ],
      }
   );
});

import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import {
   buildItineraryWithSelectedConflictResolutions,
   buildItineraryWithSelectedWildEncounters,
   getSelectedGuardiansTalks,
   getSelectedWildEncounters,
   getWildEncounterConflictIssueStartTime,
   hasUnresolvedWildEncounterConflictGroups,
   hasWildEncounterConflictSelection,
   isGuardiansTalkConflictItem,
   sortWildEncounterConflictIssuesByStartTime,
} from '../../scripts/itinerary/wizard/wildEncounterConflictResolution.js';

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

test('getWildEncounterConflictIssueStartTime uses the earliest encounter time', () => {
   assert.equal(
      getWildEncounterConflictIssueStartTime({
         items: [thirdEncounter, fourthEncounter],
      }),
      '14:00'
   );
});

test('sortWildEncounterConflictIssuesByStartTime orders groups by earliest time', () => {
   const afternoonIssue = {
      items: [thirdEncounter, fourthEncounter],
   };
   const middayIssue = {
      items: [firstEncounter, secondEncounter],
   };

   assert.deepEqual(
      sortWildEncounterConflictIssuesByStartTime([
         afternoonIssue,
         middayIssue,
      ]),
      [middayIssue, afternoonIssue]
   );
});

test('getSelectedWildEncounters returns selections from each conflict group', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [thirdEncounter] } },
   ];

   assert.deepEqual(
      getSelectedWildEncounters(conflictGroups),
      [firstEncounter, thirdEncounter]
   );
});

test('getSelectedWildEncounters returns multiple non-overlapping picks in one group', () => {
   const conflictGroups = [
      {
         selection: {
            items: [firstEncounter, thirdEncounter],
         },
      },
   ];

   assert.deepEqual(
      getSelectedWildEncounters(conflictGroups),
      [firstEncounter, thirdEncounter]
   );
});

test('getSelectedWildEncounters deduplicates the same encounter selected twice', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [firstEncounter] } },
   ];

   assert.deepEqual(
      getSelectedWildEncounters(conflictGroups),
      [firstEncounter]
   );
});

test('hasWildEncounterConflictSelection is false until a group has a selection', () => {
   const conflictGroups = [
      { selection: { items: [] } },
      { selection: { items: [thirdEncounter] } },
   ];

   assert.equal(hasWildEncounterConflictSelection([]), false);
   assert.equal(hasWildEncounterConflictSelection(conflictGroups), true);
});

test('hasUnresolvedWildEncounterConflictGroups detects partial resolution', () => {
   const conflictGroups = [
      { selection: { items: [firstEncounter] } },
      { selection: { items: [] } },
   ];

   assert.equal(hasUnresolvedWildEncounterConflictGroups([]), false);
   assert.equal(
      hasUnresolvedWildEncounterConflictGroups(conflictGroups),
      true
   );
   assert.equal(
      hasUnresolvedWildEncounterConflictGroups([
         { selection: { items: [firstEncounter] } },
         { selection: { items: [thirdEncounter] } },
      ]),
      false
   );
   assert.equal(
      hasUnresolvedWildEncounterConflictGroups([
         { selection: { items: [] } },
         { selection: { items: [] } },
      ]),
      false
   );
});

test('isGuardiansTalkConflictItem identifies guardians talk issue items', () => {
   assert.equal(isGuardiansTalkConflictItem(guardiansTalk), true);
   assert.equal(isGuardiansTalkConflictItem(firstEncounter), false);
});

test('getSelectedGuardiansTalks returns only guardians talk selections', () => {
   const conflictGroups = [
      { selection: { items: [guardiansTalk] } },
      { selection: { items: [firstEncounter] } },
   ];

   assert.deepEqual(
      getSelectedGuardiansTalks(conflictGroups),
      [guardiansTalk]
   );
});

test('buildItineraryWithSelectedConflictResolutions appends talks and encounters', () => {
   const itinerary = {
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };

   assert.deepEqual(
      buildItineraryWithSelectedConflictResolutions(
         itinerary,
         [guardiansTalk, firstEncounter]
      ),
      {
         ...itinerary,
         guardiansTalks: [guardiansTalk],
         wildEncounters: [firstEncounter],
      }
   );
});

test('buildItineraryWithSelectedWildEncounters appends all selected encounters', () => {
   const itinerary = {
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };

   assert.deepEqual(
      buildItineraryWithSelectedWildEncounters(
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

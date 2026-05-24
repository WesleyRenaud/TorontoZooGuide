import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildItineraryWithSelectedWildEncounters,
   getSelectedWildEncounters,
   hasWildEncounterConflictSelection,
} from '../../scripts/itinerary/wizard/wildEncounterConflictResolution.js';

const firstEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
};

const secondEncounter = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:45',
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

const thirdEncounter = {
   name: 'Savanna Safari',
   start_time: '14:00',
   end_time: '14:30',
   meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
};

const fourthEncounter = {
   name: 'Guardians of Gorillas',
   start_time: '14:30',
   end_time: '15:00',
   meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
};

test('getSelectedWildEncounters returns one choice per conflict group', () => {
   const conflictGroups = [
      { selection: { item: firstEncounter } },
      { selection: { item: thirdEncounter } },
   ];

   assert.deepEqual(
      getSelectedWildEncounters(conflictGroups),
      [firstEncounter, thirdEncounter]
   );
});

test('getSelectedWildEncounters deduplicates the same encounter selected twice', () => {
   const conflictGroups = [
      { selection: { item: firstEncounter } },
      { selection: { item: firstEncounter } },
   ];

   assert.deepEqual(
      getSelectedWildEncounters(conflictGroups),
      [firstEncounter]
   );
});

test('hasWildEncounterConflictSelection is false until a group has a selection', () => {
   const conflictGroups = [
      { selection: { item: null } },
      { selection: { item: thirdEncounter } },
   ];

   assert.equal(hasWildEncounterConflictSelection([]), false);
   assert.equal(hasWildEncounterConflictSelection(conflictGroups), true);
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

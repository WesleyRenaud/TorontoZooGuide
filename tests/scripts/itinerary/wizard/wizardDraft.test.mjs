import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardDraft } from '../../../../scripts/itinerary/wizard/wizardDraft.js';


test('Test_BuildWizardDraft_TestDateChange_ExpectTimesPreserved', () => {
   const arrivalTime = '09:15';
   const departureTime = '17:00';
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const attraction = 'Conservation Carousel';
   const currentDate = '2026-06-13';
   const nextDate = '2026-06-15';
   const source = {
      date: currentDate,
      arrivalTime,
      departureTime,
      animals: [animal],
      attractions: [attraction],
      guardiansTalks: [],
      wildEncounters: [],
      events: [],
   };

   const draft = WizardDraft.buildWizardDraft(source, { date: nextDate });

   assert.deepEqual(draft, {
      date: nextDate,
      arrivalTime,
      departureTime,
      animals: [animal],
      attractions: [attraction],
      guardiansTalks: source.guardiansTalks,
      wildEncounters: source.wildEncounters,
      transportations: [],
      transportationStations: [],
      events: source.events,
   });
});


test('Test_BuildWizardDraft_TestTransportations_ExpectPreserved', () => {
   const date = '2026-08-17';
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const transportation = { name: 'Zoomobile', added_as_attraction: true };
   const source = {
      date,
      animals: [animal],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [transportation],
      events: [],
   };

   const draft = WizardDraft.buildWizardDraft(source);

   assert.deepEqual(draft, {
      date,
      arrivalTime: '',
      departureTime: '',
      animals: [animal],
      attractions: source.attractions,
      guardiansTalks: source.guardiansTalks,
      wildEncounters: source.wildEncounters,
      transportations: [transportation],
      transportationStations: [],
      events: source.events,
   });
});

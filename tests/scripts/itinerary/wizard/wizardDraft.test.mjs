import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardDraft } from '../../../../scripts/itinerary/wizard/wizardDraft.js';

test('Test_BuildWizardDraft_TestDateChange_ExpectTimesPreserved', () => {
   assert.deepEqual(
      WizardDraft.buildWizardDraft(
         {
            date: '2026-06-13',
            arrivalTime: '09:15',
            departureTime: '17:00',
            animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
            attractions: ['Conservation Carousel'],
            guardiansTalks: [],
            wildEncounters: [],
            events: [],
         },
         {
            date: '2026-06-15',
         }
      ),
      {
         date: '2026-06-15',
         arrivalTime: '09:15',
         departureTime: '17:00',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
         attractions: ['Conservation Carousel'],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [],
         transportationStations: [],
         events: [],
      }
   );
});

test('Test_BuildWizardDraft_TestTransportations_ExpectPreserved', () => {
   assert.deepEqual(
      WizardDraft.buildWizardDraft({
         date: '2026-08-17',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [{ name: 'Zoomobile', added_as_attraction: true }],
         events: [],
      }),
      {
         date: '2026-08-17',
         arrivalTime: '',
         departureTime: '',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [{ name: 'Zoomobile', added_as_attraction: true }],
         transportationStations: [],
         events: [],
      }
   );
});

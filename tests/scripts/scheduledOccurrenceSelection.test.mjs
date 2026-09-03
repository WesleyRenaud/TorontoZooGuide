import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createSelectorSelectionState } from '../../scripts/itinerary/selectors/base/selectionState.js';
import { createScheduledOccurrenceMigration } from '../../scripts/itinerary/selectors/createScheduledOccurrenceSelector.js';
import {
   getGuardiansTalkId,
   readGuardiansTalkStoredFields,
} from '../../scripts/itinerary/selectors/guardiansTalkSelector/model.js';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';

function createGuardiansTalkSelectionState() {
   return createSelectorSelectionState({
      storageKey: STORAGE_KEY,
      getId: getGuardiansTalkId,
      migrateSelected: createScheduledOccurrenceMigration({
         emptyStoredFields: {
            location: '',
            start_time: '',
            end_time: '',
         },
         buildImageSrc: () => '',
         readStoredFields: readGuardiansTalkStoredFields,
         getId: getGuardiansTalkId,
      }),
      makeSelection: (row) => ({
         id: getGuardiansTalkId(row),
         name: row.name,
         location: row.location ?? '',
         start_time: row.start_time ?? '',
         end_time: row.end_time ?? '',
      }),
   });
}

test.describe('scheduled occurrence selection migration', () => {
   beforeEach(() => {
      globalThis.localStorage = createLocalStorageMock();
   });

   afterEach(() => {
      delete globalThis.localStorage;
   });

   test('API talk without id matches catalog wire id after migrate', () => {
      localStorage.setItem(
         STORAGE_KEY,
         JSON.stringify([
            {
               name: 'New World Primates',
               location: 'Americas Pavilion',
               start_time: '11:30 AM',
               end_time: '12:00 PM',
            },
         ])
      );

      const state = createGuardiansTalkSelectionState();
      const catalogRow = {
         name: 'New World Primates',
         location: 'Americas Pavilion',
         start_time: '11:30 AM',
         end_time: '12:00 PM',
      };
      const catalogId = getGuardiansTalkId(catalogRow);

      assert.equal(catalogId, 'New World Primates||11:30 AM||12:00 PM');
      assert.equal(state.isSelected(catalogId), true);
      assert.equal(state.getSelectedSnapshot()[0].id, catalogId);
   });

   test('name-only stored id is upgraded when start and end times are present', () => {
      localStorage.setItem(
         STORAGE_KEY,
         JSON.stringify([
            {
               id: 'New World Primates',
               name: 'New World Primates',
               location: 'Americas Pavilion',
               start_time: '11:30 AM',
               end_time: '12:00 PM',
            },
         ])
      );

      const state = createGuardiansTalkSelectionState();

      assert.equal(
         state.isSelected('New World Primates||11:30 AM||12:00 PM'),
         true
      );
      assert.equal(state.isSelected('New World Primates'), false);
   });
});

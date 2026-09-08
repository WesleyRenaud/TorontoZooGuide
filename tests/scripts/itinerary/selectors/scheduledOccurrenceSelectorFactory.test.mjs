import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledOccurrenceSelectorFactory } from '../../../../scripts/itinerary/selectors/scheduledOccurrenceSelectorFactory.js';

test('Test_GetOccurrenceName_TestRow_ExpectNameOrEmpty', () => {
   assert.equal(ScheduledOccurrenceSelectorFactory.getOccurrenceName({ name: 'Talk' }), 'Talk');
   assert.equal(ScheduledOccurrenceSelectorFactory.getOccurrenceName(null), '');
});

test('Test_CreateStoredOccurrenceFromString_TestBlankAndValue_ExpectNullOrStored', () => {
   assert.equal(
      ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString('  ', {
         emptyStoredFields: { location: '' },
         buildImageSrc: () => 'img',
      }),
      null
   );
   assert.deepEqual(
      ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString('Tiger Talk', {
         emptyStoredFields: { location: '' },
         buildImageSrc: (name) => `img/${name}`,
      }),
      {
         id: 'Tiger Talk',
         name: 'Tiger Talk',
         location: '',
         imageSrc: 'img/Tiger Talk',
      }
   );
});

test('Test_CreateStoredOccurrenceFromObject_TestFields_ExpectStored', () => {
   assert.equal(
      ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject(
         { name: 'Talk' },
         {
            buildImageSrc: () => 'img',
            readStoredFields: () => ({}),
            getId: () => '',
         }
      ),
      null
   );

   assert.deepEqual(
      ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject(
         {
            name: 'Talk',
            start_time: '11:00 AM',
            end_time: '11:30 AM',
            maximum_duration: 30,
            link: 'https://example.test',
            imageSrc: '',
         },
         {
            buildImageSrc: (name) => `img/${name}`,
            includeLink: true,
            readStoredFields: () => ({ location: 'Eurasia' }),
            getId: () => 'talk-1',
         }
      ),
      {
         id: 'talk-1',
         name: 'Talk',
         location: 'Eurasia',
         imageSrc: 'img/Talk',
         link: 'https://example.test',
         start_time: '11:00 AM',
         end_time: '11:30 AM',
         maximum_duration: 30,
      }
   );
});

test('Test_CreateOccurrenceSelection_TestRow_ExpectSelection', () => {
   assert.deepEqual(
      ScheduledOccurrenceSelectorFactory.createOccurrenceSelection(
         {
            end_time: '12:00 PM',
            maximum_duration: 45,
         },
         {
            getId: () => 'id-1',
            getLink: () => 'https://example.test',
            getName: () => 'Encounter',
            buildImageSrc: (name) => `img/${name}`,
            buildSelectionFields: () => ({ meeting_spot: 'Savanna' }),
            getTimeOfDay: () => '11:00 AM',
         }
      ),
      {
         id: 'id-1',
         name: 'Encounter',
         meeting_spot: 'Savanna',
         imageSrc: 'img/Encounter',
         link: 'https://example.test',
         maximum_duration: 45,
         start_time: '11:00 AM',
         end_time: '12:00 PM',
      }
   );
});

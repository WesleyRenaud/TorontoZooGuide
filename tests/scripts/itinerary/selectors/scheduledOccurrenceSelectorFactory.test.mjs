import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledOccurrenceSelectorFactory } from '../../../../scripts/itinerary/selectors/scheduledOccurrenceSelectorFactory.js';


test('Test_GetOccurrenceName_TestRow_ExpectName', () => {
   const name = 'Talk';
   const row = { name };

   const occurrenceName = ScheduledOccurrenceSelectorFactory.getOccurrenceName(row);

   assert.equal(occurrenceName, name);
});


test('Test_GetOccurrenceName_TestNull_ExpectEmpty', () => {
   const row = null;

   const occurrenceName = ScheduledOccurrenceSelectorFactory.getOccurrenceName(row);

   assert.equal(occurrenceName, '');
});


test('Test_CreateStoredOccurrenceFromString_TestBlank_ExpectNull', () => {
   const value = '  ';

   const stored = ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString(value, {
      emptyStoredFields: { location: '' },
      buildImageSrc: () => 'img',
   });

   assert.equal(stored, null);
});


test('Test_CreateStoredOccurrenceFromString_TestName_ExpectStored', () => {
   const name = 'Tiger Talk';
   const emptyStoredFields = { location: '' };
   const buildImageSrc = (value) => `img/${value}`;

   const stored = ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString(name, {
      emptyStoredFields,
      buildImageSrc,
   });

   assert.equal(stored.id, name);
   assert.equal(stored.name, name);
   assert.equal(stored.location, emptyStoredFields.location);
   assert.equal(stored.imageSrc, buildImageSrc(name));
});


test('Test_CreateStoredOccurrenceFromObject_TestMissingId_ExpectNull', () => {
   const item = { name: 'Talk' };

   const stored = ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject(
      item,
      {
         buildImageSrc: () => 'img',
         readStoredFields: () => ({}),
         getId: () => '',
      }
   );

   assert.equal(stored, null);
});


test('Test_CreateStoredOccurrenceFromObject_TestFields_ExpectStored', () => {
   const name = 'Talk';
   const startTime = '11:00 AM';
   const endTime = '11:30 AM';
   const maximumDuration = 30;
   const link = 'https://example.test';
   const location = 'Eurasia';
   const id = 'talk-1';
   const item = {
      name,
      start_time: startTime,
      end_time: endTime,
      maximum_duration: maximumDuration,
      link,
      imageSrc: '',
   };
   const buildImageSrc = (value) => `img/${value}`;

   const stored = ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject(
      item,
      {
         buildImageSrc,
         includeLink: true,
         readStoredFields: () => ({ location }),
         getId: () => id,
      }
   );

   assert.equal(stored.id, id);
   assert.equal(stored.name, name);
   assert.equal(stored.location, location);
   assert.equal(stored.imageSrc, buildImageSrc(name));
   assert.equal(stored.link, link);
   assert.equal(stored.start_time, startTime);
   assert.equal(stored.end_time, endTime);
   assert.equal(stored.maximum_duration, maximumDuration);
});


test('Test_CreateOccurrenceSelection_TestRow_ExpectSelection', () => {
   const id = 'id-1';
   const name = 'Encounter';
   const meetingSpot = 'Savanna';
   const link = 'https://example.test';
   const startTime = '11:00 AM';
   const endTime = '12:00 PM';
   const maximumDuration = 45;
   const row = {
      end_time: endTime,
      maximum_duration: maximumDuration,
   };
   const buildImageSrc = (value) => `img/${value}`;

   const selection = ScheduledOccurrenceSelectorFactory.createOccurrenceSelection(
      row,
      {
         getId: () => id,
         getLink: () => link,
         getName: () => name,
         buildImageSrc,
         buildSelectionFields: () => ({ meeting_spot: meetingSpot }),
         getTimeOfDay: () => startTime,
      }
   );

   assert.equal(selection.id, id);
   assert.equal(selection.name, name);
   assert.equal(selection.meeting_spot, meetingSpot);
   assert.equal(selection.imageSrc, buildImageSrc(name));
   assert.equal(selection.link, link);
   assert.equal(selection.maximum_duration, maximumDuration);
   assert.equal(selection.start_time, startTime);
   assert.equal(selection.end_time, endTime);
});

import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelectorStoredAttractionFactory } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorStoredAttractionFactory.js';

test('Test_CreateStoredAttractionFromString_TestName_ExpectStoredOrNull', () => {
   assert.equal(AttractionSelectorStoredAttractionFactory.createStoredAttractionFromString('  '), null);
   assert.deepEqual(
      AttractionSelectorStoredAttractionFactory.createStoredAttractionFromString('Carousel'),
      {
         id: 'Carousel',
         name: 'Carousel',
         subtitle: '',
         freeWithAdmission: false,
         seasonal: false,
         isClosed: false,
         addedAsAttraction: false,
         infoLink: null,
         imageSrc: null,
      }
   );
});

test('Test_CreateStoredAttractionFromObject_TestFields_ExpectStored', () => {
   assert.deepEqual(
      AttractionSelectorStoredAttractionFactory.createStoredAttractionFromObject({
         id: 'c1',
         name: 'Carousel',
         subtitle: 'Ride',
         freeWithAdmission: true,
         seasonal: true,
         isClosed: false,
         addedAsAttraction: true,
         infoLink: 'https://example.com',
         imageSrc: 'img.png',
      }),
      {
         id: 'c1',
         name: 'Carousel',
         subtitle: 'Ride',
         freeWithAdmission: true,
         seasonal: true,
         isClosed: false,
         addedAsAttraction: true,
         infoLink: 'https://example.com',
         imageSrc: 'img.png',
      }
   );
   assert.equal(AttractionSelectorStoredAttractionFactory.createStoredAttractionFromObject({ name: '' }), null);
});

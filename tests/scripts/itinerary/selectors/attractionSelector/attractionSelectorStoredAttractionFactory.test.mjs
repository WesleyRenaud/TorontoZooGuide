import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelectorStoredAttractionFactory } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorStoredAttractionFactory.js';


test('Test_CreateStoredAttractionFromString_TestBlank_ExpectNull', () => {
   const value = '  ';

   const stored = AttractionSelectorStoredAttractionFactory.createStoredAttractionFromString(value);

   assert.equal(stored, null);
});


test('Test_CreateStoredAttractionFromString_TestName_ExpectStored', () => {
   const name = 'Carousel';

   const stored = AttractionSelectorStoredAttractionFactory.createStoredAttractionFromString(name);

   assert.equal(stored.id, name);
   assert.equal(stored.name, name);
   assert.equal(stored.subtitle, '');
   assert.equal(stored.freeWithAdmission, false);
   assert.equal(stored.seasonal, false);
   assert.equal(stored.isClosed, false);
   assert.equal(stored.addedAsAttraction, false);
   assert.equal(stored.infoLink, null);
   assert.equal(stored.imageSrc, null);
});


test('Test_CreateStoredAttractionFromObject_TestFields_ExpectStored', () => {
   const id = 'c1';
   const name = 'Carousel';
   const subtitle = 'Ride';
   const infoLink = 'https://example.com';
   const imageSrc = 'img.png';
   const item = {
      id,
      name,
      subtitle,
      freeWithAdmission: true,
      seasonal: true,
      isClosed: false,
      addedAsAttraction: true,
      infoLink,
      imageSrc,
   };

   const stored = AttractionSelectorStoredAttractionFactory.createStoredAttractionFromObject(item);

   assert.equal(stored.id, id);
   assert.equal(stored.name, name);
   assert.equal(stored.subtitle, subtitle);
   assert.equal(stored.freeWithAdmission, item.freeWithAdmission);
   assert.equal(stored.seasonal, item.seasonal);
   assert.equal(stored.isClosed, item.isClosed);
   assert.equal(stored.addedAsAttraction, item.addedAsAttraction);
   assert.equal(stored.infoLink, infoLink);
   assert.equal(stored.imageSrc, imageSrc);
});


test('Test_CreateStoredAttractionFromObject_TestBlankName_ExpectNull', () => {
   const item = { name: '' };

   const stored = AttractionSelectorStoredAttractionFactory.createStoredAttractionFromObject(item);

   assert.equal(stored, null);
});

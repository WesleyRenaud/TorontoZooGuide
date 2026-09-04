import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelectorModel } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';

const carouselRow = {
   name: 'Conservation Carousel',
   free_with_admission: true,
   part_of_seasonal_attraction: false,
   is_closed: false,
   info_link: ' https://example.com/carousel ',
};

test('Test_GetAttractionSubtitle_TestPresentationFields_ExpectDerivedValues', () => {
   assert.equal(AttractionSelectorModel.getAttractionSubtitle(carouselRow), 'Free With Admission');
   assert.equal(
      AttractionSelectorModel.getAttractionSubtitle({ free_with_admission: false }),
      'Extra Charge'
   );
   assert.equal(
      AttractionSelectorModel.getAttractionSubtitle({
         free_with_admission: false,
         open_time: '10:00 AM',
         close_time: '4:00 PM',
      }),
      'Extra Charge  •  10:00 AM - 4:00 PM'
   );
   assert.equal(
      AttractionSelectorModel.getAttractionSubtitle({
         free_with_admission: true,
         open_time: '11:00 AM',
         close_time: '5:00 PM',
      }),
      'Free With Admission  •  11:00 AM - 5:00 PM'
   );
   assert.equal(
      AttractionSelectorModel.buildAttractionImageSrc(carouselRow),
      '../images/details/attractions/conservation-carousel.png'
   );
   assert.deepEqual(AttractionSelectorModel.makeAttractionSelection(carouselRow), {
      id: 'Conservation Carousel',
      name: 'Conservation Carousel',
      subtitle: 'Free With Admission',
      freeWithAdmission: true,
      seasonal: false,
      isClosed: false,
      addedAsAttraction: false,
      infoLink: 'https://example.com/carousel',
      imageSrc: '../images/details/attractions/conservation-carousel.png',
   });
   assert.deepEqual(
      AttractionSelectorModel.makeAttractionSelection({
         name: 'Zoomobile',
         is_also_transportation: true,
         free_with_admission: false,
      }),
      {
         id: 'Zoomobile',
         name: 'Zoomobile',
         subtitle: 'Extra Charge',
         freeWithAdmission: false,
         seasonal: false,
         isClosed: false,
         addedAsAttraction: true,
         infoLink: null,
         imageSrc: '../images/details/attractions/zoomobile.png',
      }
   );
});

test('Test_ShouldConfirmClosedAttraction_TestNewClosed_ExpectPromptOnlyWhenAdding', () => {
   const closedRow = { is_closed: true };

   assert.equal(
      AttractionSelectorModel.shouldConfirmClosedAttraction({
         row: closedRow,
         isSelected: false,
         includeClosedAttractions: true,
      }),
      true
   );
   assert.equal(
      AttractionSelectorModel.shouldConfirmClosedAttraction({
         row: closedRow,
         isSelected: true,
         includeClosedAttractions: true,
      }),
      false
   );
   assert.equal(
      AttractionSelectorModel.shouldConfirmClosedAttraction({
         row: closedRow,
         isSelected: false,
         includeClosedAttractions: false,
      }),
      false
   );
});

test('Test_ShouldConfirmAlsoTransportationAttraction_TestAdding_ExpectPromptOnlyWhenAdding', () => {
   const zoomobileRow = { is_also_transportation: true };

   assert.equal(
      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction({
         row: zoomobileRow,
         isSelected: false,
      }),
      true
   );
   assert.equal(
      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction({
         row: zoomobileRow,
         isSelected: true,
      }),
      false
   );
   assert.equal(
      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction({
         row: carouselRow,
         isSelected: false,
      }),
      false
   );
});

test('Test_BuildClosedAttractionMessage_TestMissingName_ExpectFallback', () => {
   assert.equal(
      AttractionSelectorModel.buildClosedAttractionMessage({ name: 'Zoomobile' }),
      'The Zoomobile is closed on your visit date. Do you still want to add it to your itinerary?'
   );
   assert.match(
      AttractionSelectorModel.buildClosedAttractionMessage({}),
      /This attraction is closed/
   );
});

test('Test_BuildAlsoTransportationAttractionMessage_TestZoomobile_ExpectExplainsModes', () => {
   assert.equal(
      AttractionSelectorModel.buildAlsoTransportationAttractionMessage({ name: 'Zoomobile' }),
      'The Zoomobile can be added as a transportation method to reduce walking, or as an attraction for a scenic trip around the zoo. This action will add the Zoomobile as an attraction.'
   );
});

test('Test_MigrateStoredAttractions_TestStringAndObject_ExpectNormalized', () => {
   assert.deepEqual(
      AttractionSelectorModel.migrateStoredAttractions([
         'Zoomobile',
         {
            name: '  Conservation Carousel  ',
            subtitle: '  Seasonal  ',
            freeWithAdmission: true,
            seasonal: true,
            isClosed: false,
            infoLink: ' https://example.com ',
            imageSrc: ' ../images/carousel.png ',
         },
         { name: ' ' },
      ]),
      [
         {
            id: 'Zoomobile',
            name: 'Zoomobile',
            subtitle: '',
            freeWithAdmission: false,
            seasonal: false,
            isClosed: false,
            addedAsAttraction: false,
            infoLink: null,
            imageSrc: null,
         },
         {
            id: 'Conservation Carousel',
            name: 'Conservation Carousel',
            subtitle: 'Seasonal',
            freeWithAdmission: true,
            seasonal: true,
            isClosed: false,
            addedAsAttraction: false,
            infoLink: 'https://example.com',
            imageSrc: '../images/carousel.png',
         },
      ]
   );
});

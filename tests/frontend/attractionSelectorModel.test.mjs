import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildAttractionImageSrc,
   buildClosedAttractionMessage,
   getAttractionSubtitle,
   makeAttractionSelection,
   migrateStoredAttractions,
   shouldConfirmClosedAttraction,
} from '../../scripts/itinerary/selectors/attractionSelector/model.js';

const carouselRow = {
   name: 'Conservation Carousel',
   free_with_admission: true,
   part_of_seasonal_attraction: false,
   is_closed: false,
   info_link: ' https://example.com/carousel ',
};

test('attraction selector model derives presentation fields', () => {
   assert.equal(getAttractionSubtitle(carouselRow), 'Free With Admission');
   assert.equal(
      getAttractionSubtitle({ free_with_admission: false }),
      'Extra Charge'
   );
   assert.equal(
      getAttractionSubtitle({
         free_with_admission: false,
         open_time: '10:00 AM',
         close_time: '4:00 PM',
      }),
      'Extra Charge  •  10:00 AM - 4:00 PM'
   );
   assert.equal(
      getAttractionSubtitle({
         free_with_admission: true,
         open_time: '11:00 AM',
         close_time: '5:00 PM',
      }),
      'Free With Admission  •  11:00 AM - 5:00 PM'
   );
   assert.equal(
      buildAttractionImageSrc(carouselRow),
      '../images/details/attractions/conservation-carousel.png'
   );
   assert.deepEqual(makeAttractionSelection(carouselRow), {
      id: 'Conservation Carousel',
      name: 'Conservation Carousel',
      subtitle: 'Free With Admission',
      freeWithAdmission: true,
      seasonal: false,
      isClosed: false,
      infoLink: 'https://example.com/carousel',
      imageSrc: '../images/details/attractions/conservation-carousel.png',
   });
});

test('shouldConfirmClosedAttraction only prompts for new closed attractions', () => {
   const closedRow = { is_closed: true };

   assert.equal(
      shouldConfirmClosedAttraction({
         row: closedRow,
         isSelected: false,
         includeClosedAttractions: true,
      }),
      true
   );
   assert.equal(
      shouldConfirmClosedAttraction({
         row: closedRow,
         isSelected: true,
         includeClosedAttractions: true,
      }),
      false
   );
   assert.equal(
      shouldConfirmClosedAttraction({
         row: closedRow,
         isSelected: false,
         includeClosedAttractions: false,
      }),
      false
   );
});

test('buildClosedAttractionMessage falls back when the attraction name is missing', () => {
   assert.equal(
      buildClosedAttractionMessage({ name: 'Zoomobile' }),
      'The Zoomobile is closed on your visit date. Do you still want to add it to your itinerary?'
   );
   assert.match(
      buildClosedAttractionMessage({}),
      /This attraction is closed/
   );
});

test('migrateStoredAttractions normalizes string and object entries', () => {
   assert.deepEqual(
      migrateStoredAttractions([
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
            infoLink: 'https://example.com',
            imageSrc: '../images/carousel.png',
         },
      ]
   );
});

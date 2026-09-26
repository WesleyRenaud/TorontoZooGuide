import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelectorModel } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { AttractionSelectorStoredAttractionFactory } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorStoredAttractionFactory.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';


const carouselRow = {
   name: 'Conservation Carousel',
   free_with_admission: true,
   part_of_seasonal_attraction: false,
   is_closed: false,
   info_link: ' https://example.com/carousel ',
};


test('Test_GetAttractionTitle_TestMissingName_ExpectFallback', () => {
   const row = {};

   const title = AttractionSelectorModel.getAttractionTitle(row);

   assert.equal(title, AttractionSelectorModel.DEFAULT_ATTRACTION_TITLE);
});


test('Test_BuildAttractionImageSrc_TestBlankName_ExpectNull', () => {
   const row = { name: ' ' };

   const imageSrc = AttractionSelectorModel.buildAttractionImageSrc(row);

   assert.equal(imageSrc, null);
});


test('Test_BuildAttractionImageSrc_TestMissingName_ExpectNull', () => {
   const row = {};

   const imageSrc = AttractionSelectorModel.buildAttractionImageSrc(row);

   assert.equal(imageSrc, null);
});


test('Test_GetAttractionSubtitle_TestFree_ExpectFreeCopy', () => {
   const subtitle = AttractionSelectorModel.getAttractionSubtitle(carouselRow);

   assert.equal(subtitle, Strings.search.freeWithAdmission);
});


test('Test_GetAttractionSubtitle_TestExtraCharge_ExpectExtraChargeCopy', () => {
   const row = { free_with_admission: false };

   const subtitle = AttractionSelectorModel.getAttractionSubtitle(row);

   assert.equal(subtitle, Strings.search.extraCharge);
});


test('Test_GetAttractionSubtitle_TestExtraChargeAndHours_ExpectJoined', () => {
   const openTime = '10:00 AM';
   const closeTime = '4:00 PM';
   const row = {
      free_with_admission: false,
      open_time: openTime,
      close_time: closeTime,
   };

   const subtitle = AttractionSelectorModel.getAttractionSubtitle(row);

   assert.match(subtitle, new RegExp(Strings.search.extraCharge));
   assert.match(subtitle, new RegExp(openTime));
   assert.match(subtitle, new RegExp(closeTime));
});


test('Test_GetAttractionSubtitle_TestFreeAndHours_ExpectJoined', () => {
   const openTime = '11:00 AM';
   const closeTime = '5:00 PM';
   const row = {
      free_with_admission: true,
      open_time: openTime,
      close_time: closeTime,
   };

   const subtitle = AttractionSelectorModel.getAttractionSubtitle(row);

   assert.match(subtitle, new RegExp(Strings.search.freeWithAdmission));
   assert.match(subtitle, new RegExp(openTime));
   assert.match(subtitle, new RegExp(closeTime));
});


test('Test_BuildAttractionImageSrc_TestCarousel_ExpectPath', () => {
   const imageSrc = AttractionSelectorModel.buildAttractionImageSrc(carouselRow);

   assert.equal(imageSrc, AttractionSelectorModel.buildAttractionImageSrc({
      name: carouselRow.name,
   }));
});


test('Test_MakeAttractionSelection_TestCarousel_ExpectSelection', () => {
   const selection = AttractionSelectorModel.makeAttractionSelection(carouselRow);

   assert.equal(selection.id, AttractionSelectorModel.getAttractionId(carouselRow));
   assert.equal(selection.name, carouselRow.name);
   assert.equal(selection.subtitle, AttractionSelectorModel.getAttractionSubtitle(carouselRow));
   assert.equal(selection.freeWithAdmission, carouselRow.free_with_admission);
   assert.equal(selection.seasonal, carouselRow.part_of_seasonal_attraction);
   assert.equal(selection.isClosed, carouselRow.is_closed);
   assert.equal(selection.addedAsAttraction, false);
   assert.equal(selection.infoLink, AttractionSelectorModel.getAttractionInfoLink(carouselRow));
   assert.equal(selection.imageSrc, AttractionSelectorModel.buildAttractionImageSrc(carouselRow));
});


test('Test_MakeAttractionSelection_TestAlsoTransportation_ExpectAddedAsAttraction', () => {
   const name = 'Zoomobile';
   const row = {
      name,
      is_also_transportation: true,
      free_with_admission: false,
   };

   const selection = AttractionSelectorModel.makeAttractionSelection(row);

   assert.equal(selection.id, name);
   assert.equal(selection.name, name);
   assert.equal(selection.subtitle, AttractionSelectorModel.getAttractionSubtitle(row));
   assert.equal(selection.addedAsAttraction, row.is_also_transportation);
   assert.equal(selection.imageSrc, AttractionSelectorModel.buildAttractionImageSrc(row));
});


test('Test_ShouldConfirmClosedAttraction_TestAddingClosed_ExpectTrue', () => {
   const closedRow = { is_closed: true };

   const shouldConfirm = AttractionSelectorModel.shouldConfirmClosedAttraction({
      row: closedRow,
      isSelected: false,
      includeClosedAttractions: true,
   });

   assert.equal(shouldConfirm, true);
});


test('Test_ShouldConfirmClosedAttraction_TestAlreadySelected_ExpectFalse', () => {
   const closedRow = { is_closed: true };

   const shouldConfirm = AttractionSelectorModel.shouldConfirmClosedAttraction({
      row: closedRow,
      isSelected: true,
      includeClosedAttractions: true,
   });

   assert.equal(shouldConfirm, false);
});


test('Test_ShouldConfirmClosedAttraction_TestClosedHidden_ExpectFalse', () => {
   const closedRow = { is_closed: true };

   const shouldConfirm = AttractionSelectorModel.shouldConfirmClosedAttraction({
      row: closedRow,
      isSelected: false,
      includeClosedAttractions: false,
   });

   assert.equal(shouldConfirm, false);
});


test('Test_ShouldConfirmAlsoTransportationAttraction_TestAdding_ExpectTrue', () => {
   const zoomobileRow = { is_also_transportation: true };

   const shouldConfirm = AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction({
      row: zoomobileRow,
      isSelected: false,
   });

   assert.equal(shouldConfirm, true);
});


test('Test_ShouldConfirmAlsoTransportationAttraction_TestAlreadySelected_ExpectFalse', () => {
   const zoomobileRow = { is_also_transportation: true };

   const shouldConfirm = AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction({
      row: zoomobileRow,
      isSelected: true,
   });

   assert.equal(shouldConfirm, false);
});


test('Test_ShouldConfirmAlsoTransportationAttraction_TestCarousel_ExpectFalse', () => {
   const shouldConfirm = AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction({
      row: carouselRow,
      isSelected: false,
   });

   assert.equal(shouldConfirm, false);
});


test('Test_BuildClosedAttractionMessage_TestZoomobile_ExpectNamedCopy', () => {
   const name = 'Zoomobile';
   const row = { name };

   const message = AttractionSelectorModel.buildClosedAttractionMessage(row);

   assert.equal(message, Strings.itinerary.confirmation.closedAttractionMessage(name));
});


test('Test_BuildClosedAttractionMessage_TestMissingName_ExpectFallback', () => {
   const row = {};

   const message = AttractionSelectorModel.buildClosedAttractionMessage(row);

   assert.equal(
      message,
      Strings.itinerary.confirmation.closedAttractionMessage(
         AttractionSelectorModel.CLOSED_ATTRACTION_FALLBACK_NAME
      )
   );
});


test('Test_BuildAlsoTransportationAttractionMessage_TestZoomobile_ExpectExplainsModes', () => {
   const name = 'Zoomobile';
   const row = { name };

   const message = AttractionSelectorModel.buildAlsoTransportationAttractionMessage(row);

   assert.equal(
      message,
      Strings.itinerary.confirmation.attractionAlsoTransportationMessage(name)
   );
});


test('Test_MigrateStoredAttractions_TestStringAndObject_ExpectNormalized', () => {
   const zoomobile = 'Zoomobile';
   const carousel = 'Conservation Carousel';
   const subtitle = 'Seasonal';
   const infoLink = 'https://example.com';
   const imageSrc = '../images/carousel.png';
   const items = [
      zoomobile,
      {
         name: `  ${carousel}  `,
         subtitle: `  ${subtitle}  `,
         freeWithAdmission: true,
         seasonal: true,
         isClosed: false,
         infoLink: ` ${infoLink} `,
         imageSrc: ` ${imageSrc} `,
      },
      { name: ' ' },
   ];

   const migrated = AttractionSelectorModel.migrateStoredAttractions(items);

   assert.deepEqual(
      migrated.at(Position.FIRST),
      AttractionSelectorStoredAttractionFactory.createStoredAttractionFromString(zoomobile)
   );
   assert.deepEqual(
      migrated.at(Position.SECOND),
      AttractionSelectorStoredAttractionFactory.createStoredAttractionFromObject({
         name: carousel,
         subtitle,
         freeWithAdmission: true,
         seasonal: true,
         isClosed: false,
         infoLink,
         imageSrc,
      })
   );
});

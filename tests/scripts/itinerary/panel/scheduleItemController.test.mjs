import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ItineraryEventTypes } from '../../../../scripts/itinerary/itineraryEventTypes.js';
import { ItineraryVisitDateResolver } from '../../../../scripts/itinerary/itineraryVisitDateResolver.js';
import { ScheduleItemConfirmationController } from '../../../../scripts/itinerary/panel/scheduleItemConfirmationController.js';
import { ScheduleItemController } from '../../../../scripts/itinerary/panel/scheduleItemController.js';
import { ScheduleItemSearcher } from '../../../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { ScheduleItemTypes } from '../../../../scripts/itinerary/panel/scheduleItemTypes.js';

test('Test_BuildAnimalDraftEntry_TestMissingAndEnclosure_ExpectEntryOrNull', () => {
   const originals = {
      getAnimalSpecies: AnimalSelectorModel.getAnimalSpecies,
      getAnimalExhibit: AnimalSelectorModel.getAnimalExhibit,
      getAnimalStoredEnclosureName: AnimalSelectorModel.getAnimalStoredEnclosureName,
   };

   AnimalSelectorModel.getAnimalSpecies = () => '';
   AnimalSelectorModel.getAnimalExhibit = () => 'Savanna';
   AnimalSelectorModel.getAnimalStoredEnclosureName = () => '';
   assert.equal(ScheduleItemController.buildAnimalDraftEntry({}), null);

   AnimalSelectorModel.getAnimalSpecies = () => 'Lion';
   AnimalSelectorModel.getAnimalExhibit = () => 'Savanna';
   AnimalSelectorModel.getAnimalStoredEnclosureName = () => '';
   assert.deepEqual(ScheduleItemController.buildAnimalDraftEntry({}), {
      species: 'Lion',
      exhibit: 'Savanna',
   });

   AnimalSelectorModel.getAnimalStoredEnclosureName = () => 'Yard A';
   assert.deepEqual(ScheduleItemController.buildAnimalDraftEntry({}), {
      species: 'Lion',
      exhibit: 'Savanna',
      enclosure_name: 'Yard A',
   });

   Object.assign(AnimalSelectorModel, originals);
});

test('Test_BuildAttractionDraftEntry_TestName_ExpectNameOrNull', () => {
   const original = AttractionSelectorModel.getAttractionName;
   AttractionSelectorModel.getAttractionName = () => '';
   assert.equal(ScheduleItemController.buildAttractionDraftEntry({}), null);
   AttractionSelectorModel.getAttractionName = () => 'Carousel';
   assert.equal(ScheduleItemController.buildAttractionDraftEntry({}), 'Carousel');
   AttractionSelectorModel.getAttractionName = original;
});

test('Test_BuildScheduleItemRequest_TestEventSearchAndTimes_ExpectPayload', () => {
   const originals = {
      isScheduleItemEventType: ItineraryEventTypes.isScheduleItemEventType,
      isScheduleItemSearchEnabled: ScheduleItemTypes.isScheduleItemSearchEnabled,
      getScheduleItemRowKind: ScheduleItemSearcher.getScheduleItemRowKind,
      getScheduleItemRowId: ScheduleItemSearcher.getScheduleItemRowId,
   };

   ItineraryEventTypes.isScheduleItemEventType = () => true;
   assert.deepEqual(
      ScheduleItemController.buildScheduleItemRequest('arrival', null, ['arrival'], {
         startTime: '10:00',
         durationMinutes: 30,
      }),
      {
         itemType: 'arrival',
         key: '',
         startTime: '10:00',
         durationMinutes: 30,
      }
   );

   ItineraryEventTypes.isScheduleItemEventType = () => false;
   ScheduleItemTypes.isScheduleItemSearchEnabled = () => false;
   assert.equal(ScheduleItemController.buildScheduleItemRequest('animals', null, []), null);

   ScheduleItemTypes.isScheduleItemSearchEnabled = () => true;
   assert.equal(ScheduleItemController.buildScheduleItemRequest('animals', null, []), null);

   ScheduleItemSearcher.getScheduleItemRowKind = () => 'animal';
   ScheduleItemSearcher.getScheduleItemRowId = () => 'lion||savanna';
   assert.deepEqual(
      ScheduleItemController.buildScheduleItemRequest('animals', { id: 1 }, [], {}),
      {
         itemType: 'animal',
         key: 'lion||savanna',
      }
   );

   Object.assign(ItineraryEventTypes, {
      isScheduleItemEventType: originals.isScheduleItemEventType,
   });
   ScheduleItemTypes.isScheduleItemSearchEnabled = originals.isScheduleItemSearchEnabled;
   ScheduleItemSearcher.getScheduleItemRowKind = originals.getScheduleItemRowKind;
   ScheduleItemSearcher.getScheduleItemRowId = originals.getScheduleItemRowId;
});

test('Test_ScheduleSelectedItineraryItem_TestFailureAndSuccess_ExpectResults', async () => {
   const originals = {
      resolveEffectiveScheduleItemSelection: ScheduleItemSearcher.resolveEffectiveScheduleItemSelection,
      buildScheduleItemRequest: ScheduleItemController.buildScheduleItemRequest,
      createScheduleItemSaveFailedResult: ScheduleItemConfirmationController.createScheduleItemSaveFailedResult,
      ensureItineraryVisitDate: ItineraryVisitDateResolver.ensureItineraryVisitDate,
      scheduleItineraryItemWithConfirmation: ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation,
   };
   const failed = { ok: false };

   ScheduleItemSearcher.resolveEffectiveScheduleItemSelection = () => 'animals';
   ScheduleItemController.buildScheduleItemRequest = () => null;
   ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = () => failed;

   assert.equal(
      await ScheduleItemController.scheduleSelectedItineraryItem({}, 'animals', null, []),
      failed
   );

   ScheduleItemController.buildScheduleItemRequest = () => ({ itemType: 'animal', key: 'a' });
   ItineraryVisitDateResolver.ensureItineraryVisitDate = async () => {
      throw new Error('no date');
   };
   assert.equal(
      await ScheduleItemController.scheduleSelectedItineraryItem({}, 'animals', {}, []),
      failed
   );

   ItineraryVisitDateResolver.ensureItineraryVisitDate = async () => {};
   ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = async (request) => ({
      ok: true,
      request,
   });
   assert.deepEqual(
      await ScheduleItemController.scheduleSelectedItineraryItem({}, 'animals', {}, [], {
         startTime: '11:00',
      }),
      { ok: true, request: { itemType: 'animal', key: 'a' } }
   );

   ScheduleItemSearcher.resolveEffectiveScheduleItemSelection = originals.resolveEffectiveScheduleItemSelection;
   ScheduleItemController.buildScheduleItemRequest = originals.buildScheduleItemRequest;
   ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = originals.createScheduleItemSaveFailedResult;
   ItineraryVisitDateResolver.ensureItineraryVisitDate = originals.ensureItineraryVisitDate;
   ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = originals.scheduleItineraryItemWithConfirmation;
});

import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryEventTypes } from '../../../../scripts/itinerary/itineraryEventTypes.js';
import { ItineraryVisitDateResolver } from '../../../../scripts/itinerary/itineraryVisitDateResolver.js';
import { ScheduleItemConfirmationController } from '../../../../scripts/itinerary/panel/scheduleItemConfirmationController.js';
import { ScheduleItemController } from '../../../../scripts/itinerary/panel/scheduleItemController.js';
import { ScheduleItemSearcher } from '../../../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { ScheduleItemTypes } from '../../../../scripts/itinerary/panel/scheduleItemTypes.js';
import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';


test('Test_BuildAnimalDraftEntry_TestMissingSpecies_ExpectNull', () => {
   const originals = {
      getAnimalSpecies: AnimalSelectorModel.getAnimalSpecies,
      getAnimalExhibit: AnimalSelectorModel.getAnimalExhibit,
      getAnimalStoredEnclosureName: AnimalSelectorModel.getAnimalStoredEnclosureName,
   };
   AnimalSelectorModel.getAnimalSpecies = () => '';
   AnimalSelectorModel.getAnimalExhibit = () => 'Africa Savanna';
   AnimalSelectorModel.getAnimalStoredEnclosureName = () => '';

   try {
      const entry = ScheduleItemController.buildAnimalDraftEntry({});

      assert.equal(entry, null);
   } finally {
      Object.assign(AnimalSelectorModel, originals);
   }
});


test('Test_BuildAnimalDraftEntry_TestSpeciesAndExhibit_ExpectEntry', () => {
   const originals = {
      getAnimalSpecies: AnimalSelectorModel.getAnimalSpecies,
      getAnimalExhibit: AnimalSelectorModel.getAnimalExhibit,
      getAnimalStoredEnclosureName: AnimalSelectorModel.getAnimalStoredEnclosureName,
   };
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   AnimalSelectorModel.getAnimalSpecies = () => species;
   AnimalSelectorModel.getAnimalExhibit = () => exhibit;
   AnimalSelectorModel.getAnimalStoredEnclosureName = () => '';

   try {
      const entry = ScheduleItemController.buildAnimalDraftEntry({});

      assert.deepEqual(entry, { species, exhibit });
   } finally {
      Object.assign(AnimalSelectorModel, originals);
   }
});


test('Test_BuildAnimalDraftEntry_TestEnclosure_ExpectEnclosureName', () => {
   const originals = {
      getAnimalSpecies: AnimalSelectorModel.getAnimalSpecies,
      getAnimalExhibit: AnimalSelectorModel.getAnimalExhibit,
      getAnimalStoredEnclosureName: AnimalSelectorModel.getAnimalStoredEnclosureName,
   };
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'Yard A';
   AnimalSelectorModel.getAnimalSpecies = () => species;
   AnimalSelectorModel.getAnimalExhibit = () => exhibit;
   AnimalSelectorModel.getAnimalStoredEnclosureName = () => enclosureName;

   try {
      const entry = ScheduleItemController.buildAnimalDraftEntry({});

      assert.deepEqual(entry, { species, exhibit, enclosure_name: enclosureName });
   } finally {
      Object.assign(AnimalSelectorModel, originals);
   }
});


test('Test_BuildAttractionDraftEntry_TestBlankName_ExpectNull', () => {
   const original = AttractionSelectorModel.getAttractionName;
   AttractionSelectorModel.getAttractionName = () => '';

   try {
      const entry = ScheduleItemController.buildAttractionDraftEntry({});

      assert.equal(entry, null);
   } finally {
      AttractionSelectorModel.getAttractionName = original;
   }
});


test('Test_BuildAttractionDraftEntry_TestName_ExpectName', () => {
   const original = AttractionSelectorModel.getAttractionName;
   const name = 'Conservation Carousel';
   AttractionSelectorModel.getAttractionName = () => name;

   try {
      const entry = ScheduleItemController.buildAttractionDraftEntry({});

      assert.equal(entry, name);
   } finally {
      AttractionSelectorModel.getAttractionName = original;
   }
});


test('Test_BuildScheduleItemRequest_TestEventType_ExpectPayload', () => {
   const originals = {
      isScheduleItemEventType: ItineraryEventTypes.isScheduleItemEventType,
   };
   const itemType = 'arrival';
   const startTime = '10:00';
   const durationMinutes = 30;
   ItineraryEventTypes.isScheduleItemEventType = () => true;

   try {
      const request = ScheduleItemController.buildScheduleItemRequest(itemType, null, [itemType], {
         startTime,
         durationMinutes,
      });

      assert.deepEqual(request, {
         itemType,
         key: '',
         startTime,
         durationMinutes,
      });
   } finally {
      ItineraryEventTypes.isScheduleItemEventType = originals.isScheduleItemEventType;
   }
});


test('Test_BuildScheduleItemRequest_TestSearchDisabled_ExpectNull', () => {
   const originals = {
      isScheduleItemEventType: ItineraryEventTypes.isScheduleItemEventType,
      isScheduleItemSearchEnabled: ScheduleItemTypes.isScheduleItemSearchEnabled,
   };
   ItineraryEventTypes.isScheduleItemEventType = () => false;
   ScheduleItemTypes.isScheduleItemSearchEnabled = () => false;

   try {
      const request = ScheduleItemController.buildScheduleItemRequest(
         ScheduleItemKind.ANIMAL.itemType,
         null,
         []
      );

      assert.equal(request, null);
   } finally {
      ItineraryEventTypes.isScheduleItemEventType = originals.isScheduleItemEventType;
      ScheduleItemTypes.isScheduleItemSearchEnabled = originals.isScheduleItemSearchEnabled;
   }
});


test('Test_BuildScheduleItemRequest_TestMissingRow_ExpectNull', () => {
   const originals = {
      isScheduleItemEventType: ItineraryEventTypes.isScheduleItemEventType,
      isScheduleItemSearchEnabled: ScheduleItemTypes.isScheduleItemSearchEnabled,
   };
   ItineraryEventTypes.isScheduleItemEventType = () => false;
   ScheduleItemTypes.isScheduleItemSearchEnabled = () => true;

   try {
      const request = ScheduleItemController.buildScheduleItemRequest(
         ScheduleItemKind.ANIMAL.itemType,
         null,
         []
      );

      assert.equal(request, null);
   } finally {
      ItineraryEventTypes.isScheduleItemEventType = originals.isScheduleItemEventType;
      ScheduleItemTypes.isScheduleItemSearchEnabled = originals.isScheduleItemSearchEnabled;
   }
});


test('Test_BuildScheduleItemRequest_TestSelectedRow_ExpectPayload', () => {
   const originals = {
      isScheduleItemEventType: ItineraryEventTypes.isScheduleItemEventType,
      isScheduleItemSearchEnabled: ScheduleItemTypes.isScheduleItemSearchEnabled,
      getScheduleItemRowKind: ScheduleItemSearcher.getScheduleItemRowKind,
      getScheduleItemRowId: ScheduleItemSearcher.getScheduleItemRowId,
   };
   const itemType = ScheduleItemKind.ANIMAL.kind;
   const key = 'lion||savanna';
   ItineraryEventTypes.isScheduleItemEventType = () => false;
   ScheduleItemTypes.isScheduleItemSearchEnabled = () => true;
   ScheduleItemSearcher.getScheduleItemRowKind = () => itemType;
   ScheduleItemSearcher.getScheduleItemRowId = () => key;

   try {
      const request = ScheduleItemController.buildScheduleItemRequest(
         ScheduleItemKind.ANIMAL.itemType,
         { id: 1 },
         [],
         {}
      );

      assert.deepEqual(request, { itemType, key });
   } finally {
      ItineraryEventTypes.isScheduleItemEventType = originals.isScheduleItemEventType;
      ScheduleItemTypes.isScheduleItemSearchEnabled = originals.isScheduleItemSearchEnabled;
      ScheduleItemSearcher.getScheduleItemRowKind = originals.getScheduleItemRowKind;
      ScheduleItemSearcher.getScheduleItemRowId = originals.getScheduleItemRowId;
   }
});


test('Test_ScheduleSelectedItineraryItem_TestMissingRequest_ExpectFailed', async () => {
   const originals = {
      resolveEffectiveScheduleItemSelection: ScheduleItemSearcher.resolveEffectiveScheduleItemSelection,
      buildScheduleItemRequest: ScheduleItemController.buildScheduleItemRequest,
      createScheduleItemSaveFailedResult: ScheduleItemConfirmationController.createScheduleItemSaveFailedResult,
   };
   const failed = { ok: false };
   ScheduleItemSearcher.resolveEffectiveScheduleItemSelection = () => ScheduleItemKind.ANIMAL.itemType;
   ScheduleItemController.buildScheduleItemRequest = () => null;
   ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = () => failed;

   try {
      const result = await ScheduleItemController.scheduleSelectedItineraryItem(
         {},
         ScheduleItemKind.ANIMAL.itemType,
         null,
         []
      );

      assert.equal(result, failed);
   } finally {
      ScheduleItemSearcher.resolveEffectiveScheduleItemSelection = originals.resolveEffectiveScheduleItemSelection;
      ScheduleItemController.buildScheduleItemRequest = originals.buildScheduleItemRequest;
      ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = originals.createScheduleItemSaveFailedResult;
   }
});


test('Test_ScheduleSelectedItineraryItem_TestMissingDate_ExpectFailed', async () => {
   const originals = {
      resolveEffectiveScheduleItemSelection: ScheduleItemSearcher.resolveEffectiveScheduleItemSelection,
      buildScheduleItemRequest: ScheduleItemController.buildScheduleItemRequest,
      createScheduleItemSaveFailedResult: ScheduleItemConfirmationController.createScheduleItemSaveFailedResult,
      ensureItineraryVisitDate: ItineraryVisitDateResolver.ensureItineraryVisitDate,
   };
   const failed = { ok: false };
   const request = { itemType: ScheduleItemKind.ANIMAL.kind, key: 'a' };
   ScheduleItemSearcher.resolveEffectiveScheduleItemSelection = () => ScheduleItemKind.ANIMAL.itemType;
   ScheduleItemController.buildScheduleItemRequest = () => request;
   ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = () => failed;
   ItineraryVisitDateResolver.ensureItineraryVisitDate = async () => {
      throw new Error('no date');
   };

   try {
      const result = await ScheduleItemController.scheduleSelectedItineraryItem(
         {},
         ScheduleItemKind.ANIMAL.itemType,
         {},
         []
      );

      assert.equal(result, failed);
   } finally {
      ScheduleItemSearcher.resolveEffectiveScheduleItemSelection = originals.resolveEffectiveScheduleItemSelection;
      ScheduleItemController.buildScheduleItemRequest = originals.buildScheduleItemRequest;
      ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = originals.createScheduleItemSaveFailedResult;
      ItineraryVisitDateResolver.ensureItineraryVisitDate = originals.ensureItineraryVisitDate;
   }
});


test('Test_ScheduleSelectedItineraryItem_TestSuccess_ExpectScheduled', async () => {
   const originals = {
      resolveEffectiveScheduleItemSelection: ScheduleItemSearcher.resolveEffectiveScheduleItemSelection,
      buildScheduleItemRequest: ScheduleItemController.buildScheduleItemRequest,
      ensureItineraryVisitDate: ItineraryVisitDateResolver.ensureItineraryVisitDate,
      scheduleItineraryItemWithConfirmation: ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation,
   };
   const request = { itemType: ScheduleItemKind.ANIMAL.kind, key: 'a' };
   ScheduleItemSearcher.resolveEffectiveScheduleItemSelection = () => ScheduleItemKind.ANIMAL.itemType;
   ScheduleItemController.buildScheduleItemRequest = () => request;
   ItineraryVisitDateResolver.ensureItineraryVisitDate = async () => {};
   ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = async (nextRequest) => ({
      ok: true,
      request: nextRequest,
   });

   try {
      const result = await ScheduleItemController.scheduleSelectedItineraryItem(
         {},
         ScheduleItemKind.ANIMAL.itemType,
         {},
         [],
         { startTime: '11:00' }
      );

      assert.deepEqual(result, { ok: true, request });
   } finally {
      ScheduleItemSearcher.resolveEffectiveScheduleItemSelection = originals.resolveEffectiveScheduleItemSelection;
      ScheduleItemController.buildScheduleItemRequest = originals.buildScheduleItemRequest;
      ItineraryVisitDateResolver.ensureItineraryVisitDate = originals.ensureItineraryVisitDate;
      ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = originals.scheduleItineraryItemWithConfirmation;
   }
});

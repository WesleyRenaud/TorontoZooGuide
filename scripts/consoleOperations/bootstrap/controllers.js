import { createAnimalOffDisplayController } from '../animals/controllers/animalOffDisplay.js';
import { createAnimalOnDisplayController } from '../animals/controllers/animalOnDisplay.js';
import { createAnimalSpeciesAutocompleteController } from '../animals/controllers/animalSpeciesAutocomplete.js';
import { createAnimalViewingAlertController } from '../animals/controllers/animalViewingAlert.js';
import { createAnimalVisibilityScheduleController } from '../animals/controllers/animalVisibilitySchedule.js';
import { createRemoveViewingAlertController } from '../animals/controllers/removeViewingAlert.js';
import { createRemoveVisibilityScheduleController } from '../animals/controllers/removeVisibilitySchedule.js';
import { createAttractionClosedController } from '../attractions/controllers/attractionClosed.js';
import { createAttractionOpenController } from '../attractions/controllers/attractionOpen.js';
import { createDrinkingFountainsClosedController } from '../drinkingFountains/controllers/drinkingFountainsClosed.js';
import { createDrinkingFountainsOpenController } from '../drinkingFountains/controllers/drinkingFountainsOpen.js';
import { createExhibitClosedController } from '../exhibits/controllers/exhibitClosed.js';
import { createExhibitOpenController } from '../exhibits/controllers/exhibitOpen.js';
import { createGiftShopClosedController } from '../giftShops/controllers/giftShopClosed.js';
import { createGiftShopOpenController } from '../giftShops/controllers/giftShopOpen.js';
import { createCancelGuardiansTalkOccurrenceController } from '../guardiansTalks/controllers/cancelGuardiansTalkOccurrence.js';
import { createEndGuardiansTalkScheduleController } from '../guardiansTalks/controllers/endGuardiansTalkSchedule.js';
import { createGuardiansTalkLocationFilterController } from '../guardiansTalks/controllers/guardiansTalkLocationFilter.js';
import { createGuardiansTalkOccurrenceFilterController } from '../guardiansTalks/controllers/guardiansTalkOccurrenceFilter.js';
import { createGuardiansTalkScheduleController } from '../guardiansTalks/controllers/guardiansTalkSchedule.js';
import { createRestaurantClosedController } from '../restaurants/controllers/restaurantClosed.js';
import { createRestaurantOpenController } from '../restaurants/controllers/restaurantOpen.js';
import { createRemoveRestroomAlertController } from '../restrooms/controllers/removeRestroomAlert.js';
import { createRestroomAlertController } from '../restrooms/controllers/restroomAlert.js';
import { createRestroomClosedController } from '../restrooms/controllers/restroomClosed.js';
import { createRestroomOpenController } from '../restrooms/controllers/restroomOpen.js';
import { createCreateUpdateController } from '../updates/controllers/createUpdate.js';
import { createEditUpdateController } from '../updates/controllers/editUpdate.js';
import { createEndUpdateController } from '../updates/controllers/endUpdate.js';
import { createCancelWildEncounterOccurrenceController } from '../wildEncounters/controllers/cancelWildEncounterOccurrence.js';
import { createEndWildEncounterScheduleController } from '../wildEncounters/controllers/endWildEncounterSchedule.js';
import { createWildEncounterOccurrenceFilterController } from '../wildEncounters/controllers/wildEncounterOccurrenceFilter.js';
import { createWildEncounterScheduleController } from '../wildEncounters/controllers/wildEncounterSchedule.js';
import { createZoomobileRouteController } from '../zoomobile/controllers/zoomobileRoute.js';
import { createZoomobileStationClosedController } from '../zoomobile/controllers/zoomobileStationClosed.js';
import { createZoomobileStationOpenController } from '../zoomobile/controllers/zoomobileStationOpen.js';

const ANIMAL_SPECIES_AUTOCOMPLETE_KEYS = [
   'offDisplay',
   'onDisplay',
   'visibilitySchedule',
   'removeVisibilitySchedule',
   'viewingAlert',
   'removeViewingAlert',
];

const CONTROLLER_BINDINGS = [
   {
      createController: createAnimalOffDisplayController,
      getRefs: refs => refs.animals.offDisplay,
   },
   {
      createController: createAnimalOnDisplayController,
      getRefs: refs => refs.animals.onDisplay,
   },
   {
      createController: createAnimalVisibilityScheduleController,
      getRefs: refs => refs.animals.visibilitySchedule,
   },
   {
      createController: createRemoveVisibilityScheduleController,
      getRefs: refs => refs.animals.removeVisibilitySchedule,
   },
   {
      createController: createAnimalViewingAlertController,
      getRefs: refs => refs.animals.viewingAlert,
   },
   {
      createController: createRemoveViewingAlertController,
      getRefs: refs => refs.animals.removeViewingAlert,
   },
   {
      createController: createExhibitClosedController,
      getRefs: refs => refs.exhibits.closed,
   },
   {
      createController: createExhibitOpenController,
      getRefs: refs => refs.exhibits.open,
   },
   {
      createController: createRestaurantClosedController,
      getRefs: refs => refs.restaurants.closed,
   },
   {
      createController: createRestaurantOpenController,
      getRefs: refs => refs.restaurants.open,
   },
   {
      createController: createRestroomClosedController,
      getRefs: refs => refs.restrooms.closed,
   },
   {
      createController: createRestroomOpenController,
      getRefs: refs => refs.restrooms.open,
   },
   {
      createController: createRestroomAlertController,
      getRefs: refs => refs.restrooms.alert,
   },
   {
      createController: createRemoveRestroomAlertController,
      getRefs: refs => refs.restrooms.removeAlert,
   },
   {
      createController: createGiftShopClosedController,
      getRefs: refs => refs.giftShops.closed,
   },
   {
      createController: createGiftShopOpenController,
      getRefs: refs => refs.giftShops.open,
   },
   {
      createController: createAttractionClosedController,
      getRefs: refs => refs.attractions.closed,
   },
   {
      createController: createAttractionOpenController,
      getRefs: refs => refs.attractions.open,
   },
   {
      createController: createZoomobileStationClosedController,
      getRefs: refs => refs.zoomobile.stationClosed,
   },
   {
      createController: createZoomobileStationOpenController,
      getRefs: refs => refs.zoomobile.stationOpen,
   },
   {
      createController: createZoomobileRouteController,
      getRefs: refs => refs.zoomobile.route,
   },
   {
      createController: createGuardiansTalkScheduleController,
      getRefs: refs => refs.guardiansTalks.schedule,
      getExtraOptions: ({ guardiansTalkScheduleLocationFilterController }) => ({
         talkLocationFilterController: guardiansTalkScheduleLocationFilterController,
      }),
   },
   {
      createController: createEndGuardiansTalkScheduleController,
      getRefs: refs => refs.guardiansTalks.endSchedule,
      getExtraOptions: ({ endGuardiansTalkScheduleLocationFilterController }) => ({
         talkLocationFilterController: endGuardiansTalkScheduleLocationFilterController,
      }),
   },
   {
      createController: createCancelGuardiansTalkOccurrenceController,
      getRefs: refs => refs.guardiansTalks.cancelOccurrence,
      getExtraOptions: ({
         cancelGuardiansTalkOccurrenceLocationFilterController,
         cancelGuardiansTalkOccurrenceFilterController,
      }) => ({
         talkLocationFilterController: cancelGuardiansTalkOccurrenceLocationFilterController,
         occurrenceFilterController: cancelGuardiansTalkOccurrenceFilterController,
      }),
   },
   {
      createController: createWildEncounterScheduleController,
      getRefs: refs => refs.wildEncounters.schedule,
   },
   {
      createController: createEndWildEncounterScheduleController,
      getRefs: refs => refs.wildEncounters.endSchedule,
   },
   {
      createController: createCancelWildEncounterOccurrenceController,
      getRefs: refs => refs.wildEncounters.cancelOccurrence,
      getExtraOptions: ({ wildEncounterOccurrenceFilterController }) => ({
         occurrenceFilterController: wildEncounterOccurrenceFilterController,
      }),
   },
   {
      createController: createDrinkingFountainsClosedController,
      getRefs: refs => refs.drinkingFountains.closed,
   },
   {
      createController: createDrinkingFountainsOpenController,
      getRefs: refs => refs.drinkingFountains.open,
   },
   {
      createController: createCreateUpdateController,
      getRefs: refs => refs.updates.create,
   },
   {
      createController: createEndUpdateController,
      getRefs: refs => refs.updates.end,
   },
   {
      createController: createEditUpdateController,
      getRefs: refs => refs.updates.edit,
   },
];

function initAnimalSpeciesAutocompletes(animals) {
   ANIMAL_SPECIES_AUTOCOMPLETE_KEYS.forEach(key => {
      const { speciesEl, speciesResultsEl, exhibitEl } = animals[key];

      createAnimalSpeciesAutocompleteController({
         inputEl: speciesEl,
         resultsEl: speciesResultsEl,
         exhibitEl,
      });
   });
}

function createControllerOptions({
   refs,
   activatePanel,
   getExtraOptions,
   specialControllers,
} = {}) {
   return {
      ...refs,
      activatePanel,
      ...(getExtraOptions ? getExtraOptions(specialControllers) : {}),
   };
}

function wireControllerBindings({
   refs,
   activatePanel,
   specialControllers,
} = {}) {
   CONTROLLER_BINDINGS.forEach(({ createController, getRefs, getExtraOptions }) => {
      createController(
         createControllerOptions({
            refs: getRefs(refs),
            activatePanel,
            getExtraOptions,
            specialControllers,
         })
      );
   });
}

export function createConsoleSpecialControllers({ guardiansTalks, wildEncounters }) {
   return {
      guardiansTalkScheduleLocationFilterController:
         createGuardiansTalkLocationFilterController({
            locationEl: guardiansTalks.schedule.locationEl,
            talkNameEl: guardiansTalks.schedule.talkNameEl,
         }),
      endGuardiansTalkScheduleLocationFilterController:
         createGuardiansTalkLocationFilterController({
            locationEl: guardiansTalks.endSchedule.locationEl,
            talkNameEl: guardiansTalks.endSchedule.talkNameEl,
         }),
      cancelGuardiansTalkOccurrenceLocationFilterController:
         createGuardiansTalkLocationFilterController({
            locationEl: guardiansTalks.cancelOccurrence.locationEl,
            talkNameEl: guardiansTalks.cancelOccurrence.talkNameEl,
         }),
      cancelGuardiansTalkOccurrenceFilterController:
         createGuardiansTalkOccurrenceFilterController({
            locationEl: guardiansTalks.cancelOccurrence.locationEl,
            talkNameEl: guardiansTalks.cancelOccurrence.talkNameEl,
            dateEl: guardiansTalks.cancelOccurrence.dateEl,
            timeEl: guardiansTalks.cancelOccurrence.timeEl,
         }),
      wildEncounterOccurrenceFilterController:
         createWildEncounterOccurrenceFilterController({
            wildEncounterEl: wildEncounters.cancelOccurrence.wildEncounterEl,
            dateEl: wildEncounters.cancelOccurrence.dateEl,
            timeEl: wildEncounters.cancelOccurrence.timeEl,
         }),
   };
}

export function wireConsoleOperationControllers({
   refs,
   activatePanel,
   guardiansTalkScheduleLocationFilterController,
   endGuardiansTalkScheduleLocationFilterController,
   cancelGuardiansTalkOccurrenceLocationFilterController,
   cancelGuardiansTalkOccurrenceFilterController,
   wildEncounterOccurrenceFilterController,
}) {
   initAnimalSpeciesAutocompletes(refs.animals);

   wireControllerBindings({
      refs,
      activatePanel,
      specialControllers: {
         guardiansTalkScheduleLocationFilterController,
         endGuardiansTalkScheduleLocationFilterController,
         cancelGuardiansTalkOccurrenceLocationFilterController,
         cancelGuardiansTalkOccurrenceFilterController,
         wildEncounterOccurrenceFilterController,
      },
   });
}

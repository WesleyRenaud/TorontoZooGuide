import { createAnimalOffDisplayController } from '../animals/controllers/animalOffDisplay.js';
import { createAnimalOnDisplayController } from '../animals/controllers/animalOnDisplay.js';
import { createAnimalVisibilityScheduleController } from '../animals/controllers/animalVisibilitySchedule.js';
import { createRemoveVisibilityScheduleController } from '../animals/controllers/removeVisibilitySchedule.js';
import { createAnimalViewingAlertController } from '../animals/controllers/animalViewingAlert.js';
import { createRemoveViewingAlertController } from '../animals/controllers/removeViewingAlert.js';
import { createAnimalSpeciesAutocompleteController } from '../animals/controllers/animalSpeciesAutocomplete.js';

import { createExhibitClosedController } from '../exhibits/controllers/exhibitClosed.js';
import { createExhibitOpenController } from '../exhibits/controllers/exhibitOpen.js';

import { createRestaurantClosedController } from '../restaurants/controllers/restaurantClosed.js';
import { createRestaurantOpenController } from '../restaurants/controllers/restaurantOpen.js';

import { createGiftShopClosedController } from '../giftShops/controllers/giftShopClosed.js';
import { createGiftShopOpenController } from '../giftShops/controllers/giftShopOpen.js';

import { createAttractionClosedController } from '../attractions/controllers/attractionClosed.js';
import { createAttractionOpenController } from '../attractions/controllers/attractionOpen.js';

import { createZoomobileStationClosedController } from '../zoomobile/controllers/zoomobileStationClosed.js';
import { createZoomobileStationOpenController } from '../zoomobile/controllers/zoomobileStationOpen.js';
import { createZoomobileRouteController } from '../zoomobile/controllers/zoomobileRoute.js';

import { createGuardiansTalkScheduleController } from '../guardiansTalks/controllers/guardiansTalkSchedule.js';
import { createEndGuardiansTalkScheduleController } from '../guardiansTalks/controllers/endGuardiansTalkSchedule.js';
import { createCancelGuardiansTalkOccurrenceController } from '../guardiansTalks/controllers/cancelGuardiansTalkOccurrence.js';
import { createGuardiansTalkLocationFilterController } from '../guardiansTalks/controllers/guardiansTalkLocationFilter.js';

import { createWildEncounterScheduleController } from '../wildEncounters/controllers/wildEncounterSchedule.js';
import { createEndWildEncounterScheduleController } from '../wildEncounters/controllers/endWildEncounterSchedule.js';
import { createCancelWildEncounterOccurrenceController } from '../wildEncounters/controllers/cancelWildEncounterOccurrence.js';
import { createWildEncounterOccurrenceFilterController } from '../wildEncounters/controllers/wildEncounterOccurrenceFilter.js';

function initAnimalSpeciesAutocompletes(animals) {
   [
      animals.offDisplay,
      animals.onDisplay,
      animals.visibilitySchedule,
      animals.removeVisibilitySchedule,
      animals.viewingAlert,
      animals.removeViewingAlert,
   ].forEach(({ speciesEl, speciesResultsEl, exhibitEl }) => {
      createAnimalSpeciesAutocompleteController({
         inputEl: speciesEl,
         resultsEl: speciesResultsEl,
         exhibitEl,
      });
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
   hidePanels,
   guardiansTalkScheduleLocationFilterController,
   endGuardiansTalkScheduleLocationFilterController,
   cancelGuardiansTalkOccurrenceLocationFilterController,
   wildEncounterOccurrenceFilterController,
}) {
   const {
      animals,
      exhibits,
      restaurants,
      giftShops,
      attractions,
      zoomobile,
      guardiansTalks,
      wildEncounters,
   } = refs;

   initAnimalSpeciesAutocompletes(animals);

   createAnimalOffDisplayController({
      ...animals.offDisplay,
      activatePanel,
      hidePanels,
   });

   createAnimalOnDisplayController({
      ...animals.onDisplay,
      activatePanel,
      hidePanels,
   });

   createAnimalVisibilityScheduleController({
      ...animals.visibilitySchedule,
      activatePanel,
      hidePanels,
   });

   createRemoveVisibilityScheduleController({
      ...animals.removeVisibilitySchedule,
      activatePanel,
      hidePanels,
   });

   createAnimalViewingAlertController({
      ...animals.viewingAlert,
      activatePanel,
      hidePanels,
   });

   createRemoveViewingAlertController({
      ...animals.removeViewingAlert,
      activatePanel,
      hidePanels,
   });

   createExhibitClosedController({
      ...exhibits.closed,
      activatePanel,
      hidePanels,
   });

   createExhibitOpenController({
      ...exhibits.open,
      activatePanel,
      hidePanels,
   });

   createRestaurantClosedController({
      ...restaurants.closed,
      activatePanel,
      hidePanels,
   });

   createRestaurantOpenController({
      ...restaurants.open,
      activatePanel,
      hidePanels,
   });

   createGiftShopClosedController({
      ...giftShops.closed,
      activatePanel,
      hidePanels,
   });

   createGiftShopOpenController({
      ...giftShops.open,
      activatePanel,
      hidePanels,
   });

   createAttractionClosedController({
      ...attractions.closed,
      activatePanel,
      hidePanels,
   });

   createAttractionOpenController({
      ...attractions.open,
      activatePanel,
      hidePanels,
   });

   createZoomobileStationClosedController({
      ...zoomobile.stationClosed,
      activatePanel,
      hidePanels,
   });

   createZoomobileStationOpenController({
      ...zoomobile.stationOpen,
      activatePanel,
      hidePanels,
   });

   createZoomobileRouteController({
      ...zoomobile.route,
      activatePanel,
      hidePanels,
   });

   createGuardiansTalkScheduleController({
      ...guardiansTalks.schedule,
      activatePanel,
      hidePanels,
      talkLocationFilterController: guardiansTalkScheduleLocationFilterController,
   });

   createEndGuardiansTalkScheduleController({
      ...guardiansTalks.endSchedule,
      activatePanel,
      hidePanels,
      talkLocationFilterController: endGuardiansTalkScheduleLocationFilterController,
   });

   createCancelGuardiansTalkOccurrenceController({
      ...guardiansTalks.cancelOccurrence,
      activatePanel,
      hidePanels,
      talkLocationFilterController: cancelGuardiansTalkOccurrenceLocationFilterController,
   });

   createWildEncounterScheduleController({
      ...wildEncounters.schedule,
      activatePanel,
      hidePanels,
   });

   createEndWildEncounterScheduleController({
      ...wildEncounters.endSchedule,
      activatePanel,
      hidePanels,
   });

   createCancelWildEncounterOccurrenceController({
      ...wildEncounters.cancelOccurrence,
      activatePanel,
      hidePanels,
      occurrenceFilterController: wildEncounterOccurrenceFilterController,
   });
}

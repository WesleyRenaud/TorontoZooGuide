import {
   initOffDisplayDatePickers,
   initVisibilityScheduleDateTimePickers
} from './ui/consoleDatePickers.js';

import { createAnimalOffDisplayController } from './consoleOperations/animals/controllers/animalOffDisplay.js';
import { createAnimalOnDisplayController } from './consoleOperations/animals/controllers/animalOnDisplay.js';
import { createAnimalVisibilityScheduleController } from './consoleOperations/animals/controllers/animalVisibilitySchedule.js';
import { createRemoveVisibilityScheduleController } from './consoleOperations/animals/controllers/removeVisibilitySchedule.js';
import { createAnimalViewingAlertController } from './consoleOperations/animals/controllers/animalViewingAlert.js';
import { createRemoveViewingAlertController } from './consoleOperations/animals/controllers/removeViewingAlert.js';

import { createExhibitClosedController } from './consoleOperations/exhibits/controllers/exhibitClosed.js';
import { createExhibitOpenController } from './consoleOperations/exhibits/controllers/exhibitOpen.js';

import { createRestaurantClosedController } from './consoleOperations/restaurants/controllers/restaurantClosed.js';
import { createRestaurantOpenController } from './consoleOperations/restaurants/controllers/restaurantOpen.js';

import { createGiftShopClosedController } from './consoleOperations/giftShops/controllers/giftShopClosed.js';
import { createGiftShopOpenController } from './consoleOperations/giftShops/controllers/giftShopOpen.js';

import { createAttractionClosedController } from './consoleOperations/attractions/controllers/attractionClosed.js';
import { createAttractionOpenController } from './consoleOperations/attractions/controllers/attractionOpen.js';

import { createZoomobileStationClosedController } from './consoleOperations/zoomobile/controllers/zoomobileStationClosed.js';
import { createZoomobileStationOpenController } from './consoleOperations/zoomobile/controllers/zoomobileStationOpen.js';
import { createZoomobileRouteController } from './consoleOperations/zoomobile/controllers/zoomobileRoute.js';

import { createGuardiansTalkScheduleController } from './consoleOperations/guardiansTalks/controllers/guardiansTalkSchedule.js';
import { createEndGuardiansTalkScheduleController } from './consoleOperations/guardiansTalks/controllers/endGuardiansTalkSchedule.js';
import { createCancelGuardiansTalkOccurrenceController } from './consoleOperations/guardiansTalks/controllers/cancelGuardiansTalkOccurrence.js';
import { createGuardiansTalkLocationFilterController } from './consoleOperations/guardiansTalks/controllers/guardiansTalkLocationFilter.js';

import { createWildEncounterScheduleController } from './consoleOperations/wildEncounters/controllers/wildEncounterSchedule.js';
import { createEndWildEncounterScheduleController } from './consoleOperations/wildEncounters/controllers/endWildEncounterSchedule.js';
import { createCancelWildEncounterOccurrenceController } from './consoleOperations/wildEncounters/controllers/cancelWildEncounterOccurrence.js';
import { createWildEncounterOccurrenceFilterController } from './consoleOperations/wildEncounters/controllers/wildEncounterOccurrenceFilter.js';

import { createAnimalSpeciesAutocompleteController } from './consoleOperations/animals/controllers/animalSpeciesAutocomplete.js';
import { renderConsoleOperationsPanels } from './consoleOperations/registry/panels.js';
import { getConsoleOperationsRefs } from './consoleOperations/registry/refs.js';

function activatePanel(panelEl) {
   document
      .querySelectorAll('.console-operations-panel')
      .forEach(panel => panel.classList.remove('active'));

   panelEl?.classList.add('active');

   document
      .querySelectorAll('.console-operations-menu-btn')
      .forEach(button => {
         button.classList.toggle(
            'active',
            button.dataset.panelTarget === panelEl?.id
         );
      });
}

function hidePanels() {
   document
      .querySelectorAll('.console-operations-panel')
      .forEach(panel => panel.classList.remove('active'));

   document
      .querySelectorAll('.console-operations-menu-btn')
      .forEach(button => button.classList.remove('active'));
}

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

function initConsoleDatePickers({
   animals,
   exhibits,
   restaurants,
   giftShops,
   attractions,
   zoomobile,
   guardiansTalks,
   wildEncounters,
}) {
   [
      animals.offDisplay,
      animals.viewingAlert,
      exhibits.closed,
      exhibits.open,
      restaurants.closed,
      restaurants.open,
      giftShops.closed,
      giftShops.open,
      attractions.closed,
      attractions.open,
      zoomobile.stationClosed,
      zoomobile.route,
      guardiansTalks.schedule,
      wildEncounters.schedule,
   ].forEach(({ startDateEl, endDateEl }) => {
      initOffDisplayDatePickers(startDateEl, endDateEl);
   });

   [
      guardiansTalks.endSchedule.endDateEl,
      wildEncounters.endSchedule.endDateEl,
   ].forEach(dateEl => {
      initOffDisplayDatePickers(dateEl, null);
   });

   [
      {
         startDateEl: animals.visibilitySchedule.startDateEl,
         endDateEl: animals.visibilitySchedule.endDateEl,
         startTimeEl: animals.visibilitySchedule.dailyStartTimeEl,
         endTimeEl: animals.visibilitySchedule.dailyEndTimeEl,
      },
      {
         startDateEl: guardiansTalks.schedule.startDateEl,
         endDateEl: guardiansTalks.schedule.endDateEl,
         startTimeEl: guardiansTalks.schedule.timeEl,
         endTimeEl: null,
      },
      {
         startDateEl: wildEncounters.schedule.startDateEl,
         endDateEl: wildEncounters.schedule.endDateEl,
         startTimeEl: wildEncounters.schedule.timeEl,
         endTimeEl: null,
      }
   ].forEach(({ startDateEl, endDateEl, startTimeEl, endTimeEl }) => {
      initVisibilityScheduleDateTimePickers(
         startDateEl,
         endDateEl,
         startTimeEl,
         endTimeEl
      );
   });
}

document.addEventListener('DOMContentLoaded', () => {

   const workspaceEl = document.getElementById('consoleOperationsWorkspace');

   if (!workspaceEl) {
      console.warn('[consoleOperations] missing #consoleOperationsWorkspace');
      return;
   }

   renderConsoleOperationsPanels(workspaceEl);

   const {
      animals,
      exhibits,
      restaurants,
      giftShops,
      attractions,
      zoomobile,
      guardiansTalks,
      wildEncounters,
   } = getConsoleOperationsRefs(document);

   const guardiansTalkScheduleLocationFilterController =
      createGuardiansTalkLocationFilterController({
         locationEl: guardiansTalks.schedule.locationEl,
         talkNameEl: guardiansTalks.schedule.talkNameEl,
      });

   const endGuardiansTalkScheduleLocationFilterController =
      createGuardiansTalkLocationFilterController({
         locationEl: guardiansTalks.endSchedule.locationEl,
         talkNameEl: guardiansTalks.endSchedule.talkNameEl,
      });

   const cancelGuardiansTalkOccurrenceLocationFilterController =
      createGuardiansTalkLocationFilterController({
         locationEl: guardiansTalks.cancelOccurrence.locationEl,
         talkNameEl: guardiansTalks.cancelOccurrence.talkNameEl,
      });

   const wildEncounterOccurrenceFilterController =
      createWildEncounterOccurrenceFilterController({
         wildEncounterEl: wildEncounters.cancelOccurrence.wildEncounterEl,
         dateEl: wildEncounters.cancelOccurrence.dateEl,
         timeEl: wildEncounters.cancelOccurrence.timeEl,
      });

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

   initConsoleDatePickers({
      animals,
      exhibits,
      restaurants,
      giftShops,
      attractions,
      zoomobile,
      guardiansTalks,
      wildEncounters,
   });

});

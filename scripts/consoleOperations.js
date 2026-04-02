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
import { createRestaurantOpeningScheduleController } from './consoleOperations/restaurants/controllers/restaurantOpeningSchedule.js';
import { createRemoveRestaurantOpeningScheduleController } from './consoleOperations/restaurants/controllers/removeRestaurantOpeningSchedule.js';

import { createGiftShopClosedController } from './consoleOperations/giftShops/controllers/giftShopClosed.js';
import { createGiftShopOpenController } from './consoleOperations/giftShops/controllers/giftShopOpen.js';
import { createGiftShopOpeningScheduleController } from './consoleOperations/giftShops/controllers/giftShopOpeningSchedule.js';
import { createRemoveGiftShopOpeningScheduleController } from './consoleOperations/giftShops/controllers/removeGiftShopOpeningSchedule.js';

import { createAttractionClosedController } from './consoleOperations/attractions/controllers/attractionClosed.js';
import { createAttractionOpenController } from './consoleOperations/attractions/controllers/attractionOpen.js';
import { createAttractionOpeningScheduleController } from './consoleOperations/attractions/controllers/attractionOpeningSchedule.js';
import { createRemoveAttractionOpeningScheduleController } from './consoleOperations/attractions/controllers/removeAttractionOpeningSchedule.js';

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

import { createOffDisplayPanelHtml } from './consoleOperations/animals/panels/offDisplayPanel.js';
import { createOnDisplayPanelHtml } from './consoleOperations/animals/panels/onDisplayPanel.js';
import { createVisibilitySchedulePanelHtml } from './consoleOperations/animals/panels/visibilitySchedulePanel.js';
import { createRemoveVisibilitySchedulePanelHtml } from './consoleOperations/animals/panels/removeVisibilitySchedulePanel.js';
import { createViewingAlertPanelHtml } from './consoleOperations/animals/panels/viewingAlertPanel.js';
import { createRemoveViewingAlertPanelHtml } from './consoleOperations/animals/panels/removeViewingAlertPanel.js';

import { createExhibitClosedPanelHtml } from './consoleOperations/exhibits/panels/exhibitClosedPanel.js';
import { createExhibitOpenPanelHtml } from './consoleOperations/exhibits/panels/exhibitOpenPanel.js';

import { createRestaurantClosedPanelHtml } from './consoleOperations/restaurants/panels/restaurantClosedPanel.js';
import { createRestaurantOpenPanelHtml } from './consoleOperations/restaurants/panels/restaurantOpenPanel.js';
import { createRestaurantOpeningSchedulePanelHtml } from './consoleOperations/restaurants/panels/restaurantOpeningSchedulePanel.js';
import { createRemoveRestaurantOpeningSchedulePanelHtml } from './consoleOperations/restaurants/panels/removeRestaurantOpeningSchedulePanel.js';

import { createGiftShopClosedPanelHtml } from './consoleOperations/giftShops/panels/giftShopClosedPanel.js';
import { createGiftShopOpenPanelHtml } from './consoleOperations/giftShops/panels/giftShopOpenPanel.js';
import { createGiftShopOpeningSchedulePanelHtml } from './consoleOperations/giftShops/panels/giftShopOpeningSchedulePanel.js';
import { createRemoveGiftShopOpeningSchedulePanelHtml } from './consoleOperations/giftShops/panels/removeGiftShopOpeningSchedulePanel.js';

import { createAttractionClosedPanelHtml } from './consoleOperations/attractions/panels/attractionClosedPanel.js';
import { createAttractionOpenPanelHtml } from './consoleOperations/attractions/panels/attractionOpenPanel.js';
import { createAttractionOpeningSchedulePanelHtml } from './consoleOperations/attractions/panels/attractionOpeningSchedulePanel.js';
import { createRemoveAttractionOpeningSchedulePanelHtml } from './consoleOperations/attractions/panels/removeAttractionOpeningSchedulePanel.js';

import { createZoomobileStationClosedPanelHtml } from './consoleOperations/zoomobile/panels/zoomobileStationClosedPanel.js';
import { createZoomobileStationOpenPanelHtml } from './consoleOperations/zoomobile/panels/zoomobileStationOpenPanel.js';
import { createZoomobileRoutePanelHtml } from './consoleOperations/zoomobile/panels/zoomobileRoutePanel.js';

import { createGuardiansTalkSchedulePanelHtml } from './consoleOperations/guardiansTalks/panels/guardiansTalkSchedulePanel.js';
import { createEndGuardiansTalkSchedulePanelHtml } from './consoleOperations/guardiansTalks/panels/endGuardiansTalkSchedulePanel.js';
import { createCancelGuardiansTalkOccurrencePanelHtml } from './consoleOperations/guardiansTalks/panels/cancelGuardiansTalkOccurrencePanel.js';

import { createWildEncounterSchedulePanelHtml } from './consoleOperations/wildEncounters/panels/wildEncounterSchedulePanel.js';
import { createEndWildEncounterSchedulePanelHtml } from './consoleOperations/wildEncounters/panels/endWildEncounterSchedulePanel.js';
import { createCancelWildEncounterOccurrencePanelHtml } from './consoleOperations/wildEncounters/panels/cancelWildEncounterOccurrencePanel.js';

document.addEventListener('DOMContentLoaded', () => {

   const workspaceEl = document.getElementById('consoleOperationsWorkspace');

   if (!workspaceEl) {
      console.warn('[consoleOperations] missing #consoleOperationsWorkspace');
      return;
   }

   workspaceEl.innerHTML = `
      ${createOffDisplayPanelHtml()}
      ${createOnDisplayPanelHtml()}
      ${createVisibilitySchedulePanelHtml()}
      ${createRemoveVisibilitySchedulePanelHtml()}
      ${createViewingAlertPanelHtml()}
      ${createRemoveViewingAlertPanelHtml()}
      ${createExhibitClosedPanelHtml()}
      ${createExhibitOpenPanelHtml()}
      ${createRestaurantClosedPanelHtml()}
      ${createRestaurantOpenPanelHtml()}
      ${createRestaurantOpeningSchedulePanelHtml()}
      ${createRemoveRestaurantOpeningSchedulePanelHtml()}
      ${createGiftShopClosedPanelHtml()}
      ${createGiftShopOpenPanelHtml()}
      ${createGiftShopOpeningSchedulePanelHtml()}
      ${createRemoveGiftShopOpeningSchedulePanelHtml()}
      ${createAttractionClosedPanelHtml()}
      ${createAttractionOpenPanelHtml()}
      ${createAttractionOpeningSchedulePanelHtml()}
      ${createRemoveAttractionOpeningSchedulePanelHtml()}
      ${createZoomobileStationClosedPanelHtml()}
      ${createZoomobileStationOpenPanelHtml()}
      ${createZoomobileRoutePanelHtml()}
      ${createGuardiansTalkSchedulePanelHtml()}
      ${createEndGuardiansTalkSchedulePanelHtml()}
      ${createCancelGuardiansTalkOccurrencePanelHtml()}
      ${createWildEncounterSchedulePanelHtml()}
      ${createEndWildEncounterSchedulePanelHtml()}
      ${createCancelWildEncounterOccurrencePanelHtml()}
   `;

   const offDisplayPanel = document.getElementById('offDisplayPanel');
   const onDisplayPanel = document.getElementById('onDisplayPanel');
   const visibilitySchedulePanel = document.getElementById('visibilitySchedulePanel');
   const removeVisibilitySchedulePanel = document.getElementById('removeVisibilitySchedulePanel');
   const viewingAlertPanel = document.getElementById('viewingAlertPanel');
   const removeViewingAlertPanel = document.getElementById('removeViewingAlertPanel');
   const exhibitClosedPanel = document.getElementById('exhibitClosedPanel');
   const exhibitOpenPanel = document.getElementById('exhibitOpenPanel');
   const restaurantClosedPanel = document.getElementById('restaurantClosedPanel');
   const restaurantOpenPanel = document.getElementById('restaurantOpenPanel');
   const restaurantOpeningSchedulePanel = document.getElementById('restaurantOpeningSchedulePanel');
   const removeRestaurantOpeningSchedulePanel = document.getElementById('removeRestaurantOpeningSchedulePanel');
   const giftShopClosedPanel = document.getElementById('giftShopClosedPanel');
   const giftShopOpenPanel = document.getElementById('giftShopOpenPanel');
   const giftShopOpeningSchedulePanel = document.getElementById('giftShopOpeningSchedulePanel');
   const removeGiftShopOpeningSchedulePanel = document.getElementById('removeGiftShopOpeningSchedulePanel');
   const attractionClosedPanel = document.getElementById('attractionClosedPanel');
   const attractionOpenPanel = document.getElementById('attractionOpenPanel');
   const attractionOpeningSchedulePanel = document.getElementById('attractionOpeningSchedulePanel');
   const removeAttractionOpeningSchedulePanel = document.getElementById('removeAttractionOpeningSchedulePanel');
   const zoomobileStationClosedPanel = document.getElementById('zoomobileStationClosedPanel');
   const zoomobileStationOpenPanel = document.getElementById('zoomobileStationOpenPanel');
   const zoomobileRoutePanel = document.getElementById('zoomobileRoutePanel');
   const guardiansTalkSchedulePanel = document.getElementById('guardiansTalkSchedulePanel');
   const endGuardiansTalkSchedulePanel = document.getElementById('endGuardiansTalkSchedulePanel');
   const cancelGuardiansTalkOccurrencePanel = document.getElementById('cancelGuardiansTalkOccurrencePanel');
   const wildEncounterSchedulePanel = document.getElementById('wildEncounterSchedulePanel');
   const endWildEncounterSchedulePanel = document.getElementById('endWildEncounterSchedulePanel');
   const cancelWildEncounterOccurrencePanel = document.getElementById('cancelWildEncounterOccurrencePanel');

   const offDisplaySpeciesEl = document.getElementById('offDisplaySpecies');
   const onDisplaySpeciesEl = document.getElementById('onDisplaySpecies');
   const visibilityScheduleSpeciesEl = document.getElementById('visibilityScheduleSpecies');
   const removeVisibilityScheduleSpeciesEl = document.getElementById('removeVisibilityScheduleSpecies');
   const viewingAlertSpeciesEl = document.getElementById('viewingAlertSpecies');
   const removeViewingAlertSpeciesEl = document.getElementById('removeViewingAlertSpecies');

   const offDisplaySpeciesResults = document.getElementById('offDisplaySpeciesResults');
   const onDisplaySpeciesResults = document.getElementById('onDisplaySpeciesResults');
   const visibilityScheduleSpeciesResults = document.getElementById('visibilityScheduleSpeciesResults');
   const removeVisibilityScheduleSpeciesResults = document.getElementById('removeVisibilityScheduleSpeciesResults');
   const viewingAlertSpeciesResults = document.getElementById('viewingAlertSpeciesResults');
   const removeViewingAlertSpeciesResults = document.getElementById('removeViewingAlertSpeciesResults');

   const offDisplayExhibitEl = document.getElementById('offDisplayExhibit');
   const onDisplayExhibitEl = document.getElementById('onDisplayExhibit');
   const visibilityScheduleExhibitEl = document.getElementById('visibilityScheduleExhibit');
   const removeVisibilityScheduleExhibitEl = document.getElementById('removeVisibilityScheduleExhibit');
   const viewingAlertExhibitEl = document.getElementById('viewingAlertExhibit');
   const removeViewingAlertExhibitEl = document.getElementById('removeViewingAlertExhibit');
   const exhibitClosedExhibitEl = document.getElementById('exhibitClosedExhibit');
   const exhibitOpenExhibitEl = document.getElementById('exhibitOpenExhibit');
   const restaurantClosedRestaurantEl = document.getElementById('restaurantClosedRestaurant');
   const restaurantOpenRestaurantEl = document.getElementById('restaurantOpenRestaurant');
   const restaurantOpeningScheduleRestaurantEl = document.getElementById('restaurantOpeningScheduleRestaurant');
   const removeRestaurantOpeningScheduleRestaurantEl = document.getElementById('removeRestaurantOpeningScheduleRestaurant');
   const giftShopClosedGiftShopEl = document.getElementById('giftShopClosedGiftShop');
   const giftShopOpenGiftShopEl = document.getElementById('giftShopOpenGiftShop');
   const giftShopOpeningScheduleGiftShopEl = document.getElementById('giftShopOpeningScheduleGiftShop');
   const removeGiftShopOpeningScheduleGiftShopEl = document.getElementById('removeGiftShopOpeningScheduleGiftShop');
   const attractionClosedAttractionEl = document.getElementById('attractionClosedAttraction');
   const attractionOpenAttractionEl = document.getElementById('attractionOpenAttraction');
   const attractionOpeningScheduleAttractionEl = document.getElementById('attractionOpeningScheduleAttraction');
   const removeAttractionOpeningScheduleAttractionEl = document.getElementById('removeAttractionOpeningScheduleAttraction');
   const zoomobileStationClosedZoomobileStationEl = document.getElementById('zoomobileStationClosedZoomobileStation');
   const zoomobileStationOpenZoomobileStationEl = document.getElementById('zoomobileStationOpenZoomobileStation');
   const zoomobileRouteSummerEl = document.getElementById('zoomobileRouteSummer');
   const zoomobileRouteWinterEl = document.getElementById('zoomobileRouteWinter');
   const guardiansTalkScheduleLocationEl = document.getElementById('guardiansTalkScheduleLocation');
   const guardiansTalkScheduleTalkNameEl = document.getElementById('guardiansTalkScheduleTalkName');
   const endGuardiansTalkScheduleLocationEl = document.getElementById('endGuardiansTalkScheduleLocation');
   const endGuardiansTalkScheduleTalkNameEl = document.getElementById('endGuardiansTalkScheduleTalkName');
   const cancelGuardiansTalkOccurrenceLocationEl = document.getElementById('cancelGuardiansTalkOccurrenceLocation');
   const cancelGuardiansTalkOccurrenceTalkNameEl = document.getElementById('cancelGuardiansTalkOccurrenceTalkName');
   const wildEncounterScheduleNameEl = document.getElementById('wildEncounterScheduleName');
   const endWildEncounterScheduleNameEl = document.getElementById('endWildEncounterScheduleName');
   const cancelWildEncounterOccurrenceNameEl = document.getElementById('cancelWildEncounterOccurrenceName');

   const offDisplayStartDateEl = document.getElementById('offDisplayStartDate');
   const offDisplayEndDateEl = document.getElementById('offDisplayEndDate');

   const visibilityScheduleStartDateEl = document.getElementById('visibilityScheduleStartDate');
   const visibilityScheduleEndDateEl = document.getElementById('visibilityScheduleEndDate');
   const visibilityScheduleDailyStartTimeEl = document.getElementById('visibilityScheduleDailyStartTime');
   const visibilityScheduleDailyEndTimeEl = document.getElementById('visibilityScheduleDailyEndTime');

   const viewingAlertStartDateEl = document.getElementById('viewingAlertStartDate');
   const viewingAlertEndDateEl = document.getElementById('viewingAlertEndDate');

   const exhibitClosedStartDateEl = document.getElementById('exhibitClosedStartDate');
   const exhibitClosedEndDateEl = document.getElementById('exhibitClosedEndDate');

   const restaurantClosedStartDateEl = document.getElementById('restaurantClosedStartDate');
   const restaurantClosedEndDateEl = document.getElementById('restaurantClosedEndDate');

   const restaurantOpeningSchedulePresetEl = document.getElementById('restaurantOpeningSchedulePreset');
   const restaurantOpeningScheduleStartDateEl = document.getElementById('restaurantOpeningScheduleStartDate');
   const restaurantOpeningScheduleEndDateEl = document.getElementById('restaurantOpeningScheduleEndDate');
   const restaurantOpeningScheduleMondayEl = document.getElementById('restaurantOpeningScheduleMonday');
   const restaurantOpeningScheduleTuesdayEl = document.getElementById('restaurantOpeningScheduleTuesday');
   const restaurantOpeningScheduleWednesdayEl = document.getElementById('restaurantOpeningScheduleWednesday');
   const restaurantOpeningScheduleThursdayEl = document.getElementById('restaurantOpeningScheduleThursday');
   const restaurantOpeningScheduleFridayEl = document.getElementById('restaurantOpeningScheduleFriday');
   const restaurantOpeningScheduleSaturdayEl = document.getElementById('restaurantOpeningScheduleSaturday');
   const restaurantOpeningScheduleSundayEl = document.getElementById('restaurantOpeningScheduleSunday');
   const restaurantOpeningScheduleHolidaysOnlyEl = document.getElementById('restaurantOpeningScheduleHolidaysOnly');

   const giftShopClosedStartDateEl = document.getElementById('giftShopClosedStartDate');
   const giftShopClosedEndDateEl = document.getElementById('giftShopClosedEndDate');

   const giftShopOpeningSchedulePresetEl = document.getElementById('giftShopOpeningSchedulePreset');
   const giftShopOpeningScheduleStartDateEl = document.getElementById('giftShopOpeningScheduleStartDate');
   const giftShopOpeningScheduleEndDateEl = document.getElementById('giftShopOpeningScheduleEndDate');
   const giftShopOpeningScheduleMondayEl = document.getElementById('giftShopOpeningScheduleMonday');
   const giftShopOpeningScheduleTuesdayEl = document.getElementById('giftShopOpeningScheduleTuesday');
   const giftShopOpeningScheduleWednesdayEl = document.getElementById('giftShopOpeningScheduleWednesday');
   const giftShopOpeningScheduleThursdayEl = document.getElementById('giftShopOpeningScheduleThursday');
   const giftShopOpeningScheduleFridayEl = document.getElementById('giftShopOpeningScheduleFriday');
   const giftShopOpeningScheduleSaturdayEl = document.getElementById('giftShopOpeningScheduleSaturday');
   const giftShopOpeningScheduleSundayEl = document.getElementById('giftShopOpeningScheduleSunday');
   const giftShopOpeningScheduleHolidaysOnlyEl = document.getElementById('giftShopOpeningScheduleHolidaysOnly');

   const attractionClosedStartDateEl = document.getElementById('attractionClosedStartDate');
   const attractionClosedEndDateEl = document.getElementById('attractionClosedEndDate');

   const attractionOpeningSchedulePresetEl = document.getElementById('attractionOpeningSchedulePreset');
   const attractionOpeningScheduleStartDateEl = document.getElementById('attractionOpeningScheduleStartDate');
   const attractionOpeningScheduleEndDateEl = document.getElementById('attractionOpeningScheduleEndDate');
   const attractionOpeningScheduleMondayEl = document.getElementById('attractionOpeningScheduleMonday');
   const attractionOpeningScheduleTuesdayEl = document.getElementById('attractionOpeningScheduleTuesday');
   const attractionOpeningScheduleWednesdayEl = document.getElementById('attractionOpeningScheduleWednesday');
   const attractionOpeningScheduleThursdayEl = document.getElementById('attractionOpeningScheduleThursday');
   const attractionOpeningScheduleFridayEl = document.getElementById('attractionOpeningScheduleFriday');
   const attractionOpeningScheduleSaturdayEl = document.getElementById('attractionOpeningScheduleSaturday');
   const attractionOpeningScheduleSundayEl = document.getElementById('attractionOpeningScheduleSunday');
   const attractionOpeningScheduleHolidaysOnlyEl = document.getElementById('attractionOpeningScheduleHolidaysOnly');

   const zoomobileStationClosedStartDateEl = document.getElementById('zoomobileStationClosedStartDate');
   const zoomobileStationClosedEndDateEl = document.getElementById('zoomobileStationClosedEndDate');

   const guardiansTalkScheduleStartDateEl = document.getElementById('guardiansTalkScheduleStartDate');
   const guardiansTalkScheduleEndDateEl = document.getElementById('guardiansTalkScheduleEndDate');
   const guardiansTalkScheduleTimeEl = document.getElementById('guardiansTalkScheduleTime');
   const guardiansTalkScheduleMondayEl = document.getElementById('guardiansTalkScheduleMonday');
   const guardiansTalkScheduleTuesdayEl = document.getElementById('guardiansTalkScheduleTuesday');
   const guardiansTalkScheduleWednesdayEl = document.getElementById('guardiansTalkScheduleWednesday');
   const guardiansTalkScheduleThursdayEl = document.getElementById('guardiansTalkScheduleThursday');
   const guardiansTalkScheduleFridayEl = document.getElementById('guardiansTalkScheduleFriday');
   const guardiansTalkScheduleSaturdayEl = document.getElementById('guardiansTalkScheduleSaturday');
   const guardiansTalkScheduleSundayEl = document.getElementById('guardiansTalkScheduleSunday');

   const endGuardiansTalkScheduleEndDateEl = document.getElementById('endGuardiansTalkScheduleEndDate');

   const cancelGuardiansTalkOccurrenceDateEl = document.getElementById('cancelGuardiansTalkOccurrenceDate');
   const cancelGuardiansTalkOccurrenceTimeEl = document.getElementById('cancelGuardiansTalkOccurrenceTime');

   const wildEncounterScheduleStartDateEl = document.getElementById('wildEncounterScheduleStartDate');
   const wildEncounterScheduleEndDateEl = document.getElementById('wildEncounterScheduleEndDate');
   const wildEncounterScheduleTimeEl = document.getElementById('wildEncounterScheduleTime');
   const wildEncounterScheduleMondayEl = document.getElementById('wildEncounterScheduleMonday');
   const wildEncounterScheduleTuesdayEl = document.getElementById('wildEncounterScheduleTuesday');
   const wildEncounterScheduleWednesdayEl = document.getElementById('wildEncounterScheduleWednesday');
   const wildEncounterScheduleThursdayEl = document.getElementById('wildEncounterScheduleThursday');
   const wildEncounterScheduleFridayEl = document.getElementById('wildEncounterScheduleFriday');
   const wildEncounterScheduleSaturdayEl = document.getElementById('wildEncounterScheduleSaturday');
   const wildEncounterScheduleSundayEl = document.getElementById('wildEncounterScheduleSunday');

   const endWildEncounterScheduleDateEl = document.getElementById('endWildEncounterScheduleDate');

   const cancelWildEncounterOccurrenceDateEl = document.getElementById('cancelWildEncounterOccurrenceDate');
   const cancelWildEncounterOccurrenceTimeEl = document.getElementById('cancelWildEncounterOccurrenceTime');

   const guardiansTalkScheduleLocationFilterController =
      createGuardiansTalkLocationFilterController({
         locationEl: guardiansTalkScheduleLocationEl,
         talkNameEl: guardiansTalkScheduleTalkNameEl,
      });

   const endGuardiansTalkScheduleLocationFilterController =
      createGuardiansTalkLocationFilterController({
         locationEl: endGuardiansTalkScheduleLocationEl,
         talkNameEl: endGuardiansTalkScheduleTalkNameEl,
      });

   const cancelGuardiansTalkOccurrenceLocationFilterController =
      createGuardiansTalkLocationFilterController({
         locationEl: cancelGuardiansTalkOccurrenceLocationEl,
         talkNameEl: cancelGuardiansTalkOccurrenceTalkNameEl,
      });

   const wildEncounterOccurrenceFilterController =
      createWildEncounterOccurrenceFilterController({
         wildEncounterEl: cancelWildEncounterOccurrenceNameEl,
         dateEl: cancelWildEncounterOccurrenceDateEl,
         timeEl: cancelWildEncounterOccurrenceTimeEl,
      });

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

   createAnimalSpeciesAutocompleteController({
      inputEl: offDisplaySpeciesEl,
      resultsEl: offDisplaySpeciesResults,
      exhibitEl: offDisplayExhibitEl,
   });

   createAnimalSpeciesAutocompleteController({
      inputEl: onDisplaySpeciesEl,
      resultsEl: onDisplaySpeciesResults,
      exhibitEl: onDisplayExhibitEl,
   });

   createAnimalSpeciesAutocompleteController({
      inputEl: visibilityScheduleSpeciesEl,
      resultsEl: visibilityScheduleSpeciesResults,
      exhibitEl: visibilityScheduleExhibitEl,
   });

   createAnimalSpeciesAutocompleteController({
      inputEl: removeVisibilityScheduleSpeciesEl,
      resultsEl: removeVisibilityScheduleSpeciesResults,
      exhibitEl: removeVisibilityScheduleExhibitEl,
   });

   createAnimalSpeciesAutocompleteController({
      inputEl: viewingAlertSpeciesEl,
      resultsEl: viewingAlertSpeciesResults,
      exhibitEl: viewingAlertExhibitEl,
   });

   createAnimalSpeciesAutocompleteController({
      inputEl: removeViewingAlertSpeciesEl,
      resultsEl: removeViewingAlertSpeciesResults,
      exhibitEl: removeViewingAlertExhibitEl,
   });

   createAnimalOffDisplayController({
      showButtonEl: document.getElementById('showOffDisplayForm'),
      panelEl: offDisplayPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitOffDisplay'),
      statusEl: document.getElementById('offDisplayStatus'),
      speciesEl: offDisplaySpeciesEl,
      exhibitEl: offDisplayExhibitEl,
      startDateEl: offDisplayStartDateEl,
      endDateEl: offDisplayEndDateEl,
      messageEl: document.getElementById('offDisplayMessage'),
      activatePanel,
      hidePanels,
   });

   createAnimalOnDisplayController({
      showButtonEl: document.getElementById('showOnDisplayForm'),
      panelEl: onDisplayPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitOnDisplay'),
      statusEl: document.getElementById('onDisplayStatus'),
      speciesEl: onDisplaySpeciesEl,
      exhibitEl: onDisplayExhibitEl,
      activatePanel,
      hidePanels,
   });

   createAnimalVisibilityScheduleController({
      showButtonEl: document.getElementById('showVisibilityScheduleForm'),
      panelEl: visibilitySchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitVisibilitySchedule'),
      statusEl: document.getElementById('visibilityScheduleStatus'),
      speciesEl: visibilityScheduleSpeciesEl,
      exhibitEl: visibilityScheduleExhibitEl,
      startDateEl: visibilityScheduleStartDateEl,
      endDateEl: visibilityScheduleEndDateEl,
      dailyStartTimeEl: visibilityScheduleDailyStartTimeEl,
      dailyEndTimeEl: visibilityScheduleDailyEndTimeEl,
      messageEl: document.getElementById('visibilityScheduleMessage'),
      activatePanel,
      hidePanels,
   });

   createRemoveVisibilityScheduleController({
      showButtonEl: document.getElementById('showRemoveVisibilityScheduleForm'),
      panelEl: removeVisibilitySchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitRemoveVisibilitySchedule'),
      statusEl: document.getElementById('removeVisibilityScheduleStatus'),
      speciesEl: removeVisibilityScheduleSpeciesEl,
      exhibitEl: removeVisibilityScheduleExhibitEl,
      activatePanel,
      hidePanels,
   });

   createAnimalViewingAlertController({
      showButtonEl: document.getElementById('showViewingAlertForm'),
      panelEl: viewingAlertPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitViewingAlert'),
      statusEl: document.getElementById('viewingAlertStatus'),
      speciesEl: viewingAlertSpeciesEl,
      exhibitEl: viewingAlertExhibitEl,
      startDateEl: viewingAlertStartDateEl,
      endDateEl: viewingAlertEndDateEl,
      messageEl: document.getElementById('viewingAlertMessage'),
      activatePanel,
      hidePanels,
   });

   createRemoveViewingAlertController({
      showButtonEl: document.getElementById('showRemoveViewingAlertForm'),
      panelEl: removeViewingAlertPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitRemoveViewingAlert'),
      statusEl: document.getElementById('removeViewingAlertStatus'),
      speciesEl: removeViewingAlertSpeciesEl,
      exhibitEl: removeViewingAlertExhibitEl,
      activatePanel,
      hidePanels,
   });

   createExhibitClosedController({
      showButtonEl: document.getElementById('showExhibitClosedForm'),
      panelEl: exhibitClosedPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitExhibitClosed'),
      statusEl: document.getElementById('exhibitClosedStatus'),
      exhibitEl: exhibitClosedExhibitEl,
      startDateEl: exhibitClosedStartDateEl,
      endDateEl: exhibitClosedEndDateEl,
      messageEl: document.getElementById('exhibitClosedMessage'),
      activatePanel,
      hidePanels,
   });

   createExhibitOpenController({
      showButtonEl: document.getElementById('showExhibitOpenForm'),
      panelEl: exhibitOpenPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitExhibitOpen'),
      statusEl: document.getElementById('exhibitOpenStatus'),
      exhibitEl: exhibitOpenExhibitEl,
      activatePanel,
      hidePanels,
   });

   createRestaurantClosedController({
      showButtonEl: document.getElementById('showRestaurantClosedForm'),
      panelEl: restaurantClosedPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitRestaurantClosed'),
      statusEl: document.getElementById('restaurantClosedStatus'),
      restaurantEl: restaurantClosedRestaurantEl,
      startDateEl: restaurantClosedStartDateEl,
      endDateEl: restaurantClosedEndDateEl,
      messageEl: document.getElementById('restaurantClosedMessage'),
      activatePanel,
      hidePanels,
   });

   createRestaurantOpenController({
      showButtonEl: document.getElementById('showRestaurantOpenForm'),
      panelEl: restaurantOpenPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitRestaurantOpen'),
      statusEl: document.getElementById('restaurantOpenStatus'),
      restaurantEl: restaurantOpenRestaurantEl,
      activatePanel,
      hidePanels,
   });

   createRestaurantOpeningScheduleController({
      showButtonEl: document.getElementById('showRestaurantOpeningScheduleForm'),
      panelEl: restaurantOpeningSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitRestaurantOpeningSchedule'),
      statusEl: document.getElementById('restaurantOpeningScheduleStatus'),
      restaurantEl: restaurantOpeningScheduleRestaurantEl,
      presetEl: restaurantOpeningSchedulePresetEl,
      startDateEl: restaurantOpeningScheduleStartDateEl,
      endDateEl: restaurantOpeningScheduleEndDateEl,
      mondayEl: restaurantOpeningScheduleMondayEl,
      tuesdayEl: restaurantOpeningScheduleTuesdayEl,
      wednesdayEl: restaurantOpeningScheduleWednesdayEl,
      thursdayEl: restaurantOpeningScheduleThursdayEl,
      fridayEl: restaurantOpeningScheduleFridayEl,
      saturdayEl: restaurantOpeningScheduleSaturdayEl,
      sundayEl: restaurantOpeningScheduleSundayEl,
      holidaysOnlyEl: restaurantOpeningScheduleHolidaysOnlyEl,
      messageEl: document.getElementById('restaurantOpeningScheduleMessage'),
      activatePanel,
      hidePanels,
   });

   createRemoveRestaurantOpeningScheduleController({
      showButtonEl: document.getElementById('showRemoveRestaurantOpeningScheduleForm'),
      panelEl: removeRestaurantOpeningSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitRemoveRestaurantOpeningSchedule'),
      statusEl: document.getElementById('removeRestaurantOpeningScheduleStatus'),
      restaurantEl: removeRestaurantOpeningScheduleRestaurantEl,
      activatePanel,
      hidePanels,
   });

   createGiftShopClosedController({
      showButtonEl: document.getElementById('showGiftShopClosedForm'),
      panelEl: giftShopClosedPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitGiftShopClosed'),
      statusEl: document.getElementById('giftShopClosedStatus'),
      giftShopEl: giftShopClosedGiftShopEl,
      startDateEl: giftShopClosedStartDateEl,
      endDateEl: giftShopClosedEndDateEl,
      messageEl: document.getElementById('giftShopClosedMessage'),
      activatePanel,
      hidePanels,
   });

   createGiftShopOpenController({
      showButtonEl: document.getElementById('showGiftShopOpenForm'),
      panelEl: giftShopOpenPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitGiftShopOpen'),
      statusEl: document.getElementById('giftShopOpenStatus'),
      giftShopEl: giftShopOpenGiftShopEl,
      activatePanel,
      hidePanels,
   });

   createGiftShopOpeningScheduleController({
      showButtonEl: document.getElementById('showGiftShopOpeningScheduleForm'),
      panelEl: giftShopOpeningSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitGiftShopOpeningSchedule'),
      statusEl: document.getElementById('giftShopOpeningScheduleStatus'),
      giftShopEl: giftShopOpeningScheduleGiftShopEl,
      presetEl: giftShopOpeningSchedulePresetEl,
      startDateEl: giftShopOpeningScheduleStartDateEl,
      endDateEl: giftShopOpeningScheduleEndDateEl,
      mondayEl: giftShopOpeningScheduleMondayEl,
      tuesdayEl: giftShopOpeningScheduleTuesdayEl,
      wednesdayEl: giftShopOpeningScheduleWednesdayEl,
      thursdayEl: giftShopOpeningScheduleThursdayEl,
      fridayEl: giftShopOpeningScheduleFridayEl,
      saturdayEl: giftShopOpeningScheduleSaturdayEl,
      sundayEl: giftShopOpeningScheduleSundayEl,
      holidaysOnlyEl: giftShopOpeningScheduleHolidaysOnlyEl,
      messageEl: document.getElementById('giftShopOpeningScheduleMessage'),
      activatePanel,
      hidePanels,
   });

   createRemoveGiftShopOpeningScheduleController({
      showButtonEl: document.getElementById('showRemoveGiftShopOpeningScheduleForm'),
      panelEl: removeGiftShopOpeningSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitRemoveGiftShopOpeningSchedule'),
      statusEl: document.getElementById('removeGiftShopOpeningScheduleStatus'),
      giftShopEl: removeGiftShopOpeningScheduleGiftShopEl,
      activatePanel,
      hidePanels,
   });

   createAttractionClosedController({
      showButtonEl: document.getElementById('showAttractionClosedForm'),
      panelEl: attractionClosedPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitAttractionClosed'),
      statusEl: document.getElementById('attractionClosedStatus'),
      attractionEl: attractionClosedAttractionEl,
      startDateEl: attractionClosedStartDateEl,
      endDateEl: attractionClosedEndDateEl,
      messageEl: document.getElementById('attractionClosedMessage'),
      activatePanel,
      hidePanels,
   });

   createAttractionOpenController({
      showButtonEl: document.getElementById('showAttractionOpenForm'),
      panelEl: attractionOpenPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitAttractionOpen'),
      statusEl: document.getElementById('attractionOpenStatus'),
      attractionEl: attractionOpenAttractionEl,
      activatePanel,
      hidePanels,
   });

   createAttractionOpeningScheduleController({
      showButtonEl: document.getElementById('showAttractionOpeningScheduleForm'),
      panelEl: attractionOpeningSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitAttractionOpeningSchedule'),
      statusEl: document.getElementById('attractionOpeningScheduleStatus'),
      attractionEl: attractionOpeningScheduleAttractionEl,
      presetEl: attractionOpeningSchedulePresetEl,
      startDateEl: attractionOpeningScheduleStartDateEl,
      endDateEl: attractionOpeningScheduleEndDateEl,
      mondayEl: attractionOpeningScheduleMondayEl,
      tuesdayEl: attractionOpeningScheduleTuesdayEl,
      wednesdayEl: attractionOpeningScheduleWednesdayEl,
      thursdayEl: attractionOpeningScheduleThursdayEl,
      fridayEl: attractionOpeningScheduleFridayEl,
      saturdayEl: attractionOpeningScheduleSaturdayEl,
      sundayEl: attractionOpeningScheduleSundayEl,
      holidaysOnlyEl: attractionOpeningScheduleHolidaysOnlyEl,
      messageEl: document.getElementById('attractionOpeningScheduleMessage'),
      activatePanel,
      hidePanels,
   });

   createRemoveAttractionOpeningScheduleController({
      showButtonEl: document.getElementById('showRemoveAttractionOpeningScheduleForm'),
      panelEl: removeAttractionOpeningSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitRemoveAttractionOpeningSchedule'),
      statusEl: document.getElementById('removeAttractionOpeningScheduleStatus'),
      attractionEl: removeAttractionOpeningScheduleAttractionEl,
      activatePanel,
      hidePanels,
   });

   createZoomobileStationClosedController({
      showButtonEl: document.getElementById('showZoomobileStationClosedForm'),
      panelEl: zoomobileStationClosedPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitZoomobileStationClosed'),
      statusEl: document.getElementById('zoomobileStationClosedStatus'),
      zoomobileStationEl: zoomobileStationClosedZoomobileStationEl,
      startDateEl: zoomobileStationClosedStartDateEl,
      endDateEl: zoomobileStationClosedEndDateEl,
      messageEl: document.getElementById('zoomobileStationClosedMessage'),
      activatePanel,
      hidePanels,
   });

   createZoomobileStationOpenController({
      showButtonEl: document.getElementById('showZoomobileStationOpenForm'),
      panelEl: zoomobileStationOpenPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitZoomobileStationOpen'),
      statusEl: document.getElementById('zoomobileStationOpenStatus'),
      zoomobileStationEl: zoomobileStationOpenZoomobileStationEl,
      activatePanel,
      hidePanels,
   });

   createZoomobileRouteController({
      showButtonEl: document.getElementById('showZoomobileRouteForm'),
      panelEl: zoomobileRoutePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitZoomobileRoute'),
      statusEl: document.getElementById('zoomobileRouteStatus'),
      summerRouteEl: zoomobileRouteSummerEl,
      winterRouteEl: zoomobileRouteWinterEl,
      activatePanel,
      hidePanels,
   });

   createGuardiansTalkScheduleController({
      showButtonEl: document.getElementById('showGuardiansTalkScheduleForm'),
      panelEl: guardiansTalkSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitGuardiansTalkSchedule'),
      statusEl: document.getElementById('guardiansTalkScheduleStatus'),
      talkNameEl: guardiansTalkScheduleTalkNameEl,
      locationEl: guardiansTalkScheduleLocationEl,
      startDateEl: guardiansTalkScheduleStartDateEl,
      endDateEl: guardiansTalkScheduleEndDateEl,
      timeEl: guardiansTalkScheduleTimeEl,
      mondayEl: guardiansTalkScheduleMondayEl,
      tuesdayEl: guardiansTalkScheduleTuesdayEl,
      wednesdayEl: guardiansTalkScheduleWednesdayEl,
      thursdayEl: guardiansTalkScheduleThursdayEl,
      fridayEl: guardiansTalkScheduleFridayEl,
      saturdayEl: guardiansTalkScheduleSaturdayEl,
      sundayEl: guardiansTalkScheduleSundayEl,
      messageEl: document.getElementById('guardiansTalkScheduleMessage'),
      activatePanel,
      hidePanels,
      talkLocationFilterController: guardiansTalkScheduleLocationFilterController,
   });

   createEndGuardiansTalkScheduleController({
      showButtonEl: document.getElementById('showEndGuardiansTalkScheduleForm'),
      panelEl: endGuardiansTalkSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitEndGuardiansTalkSchedule'),
      statusEl: document.getElementById('endGuardiansTalkScheduleStatus'),
      talkNameEl: endGuardiansTalkScheduleTalkNameEl,
      locationEl: endGuardiansTalkScheduleLocationEl,
      endDateEl: endGuardiansTalkScheduleEndDateEl,
      activatePanel,
      hidePanels,
      talkLocationFilterController: endGuardiansTalkScheduleLocationFilterController,
   });

   createCancelGuardiansTalkOccurrenceController({
      showButtonEl: document.getElementById('showCancelGuardiansTalkOccurrenceForm'),
      panelEl: cancelGuardiansTalkOccurrencePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitCancelGuardiansTalkOccurrence'),
      statusEl: document.getElementById('cancelGuardiansTalkOccurrenceStatus'),
      talkNameEl: cancelGuardiansTalkOccurrenceTalkNameEl,
      locationEl: cancelGuardiansTalkOccurrenceLocationEl,
      dateEl: cancelGuardiansTalkOccurrenceDateEl,
      timeEl: cancelGuardiansTalkOccurrenceTimeEl,
      activatePanel,
      hidePanels,
      talkLocationFilterController: cancelGuardiansTalkOccurrenceLocationFilterController,
   });

   createWildEncounterScheduleController({
      showButtonEl: document.getElementById('showWildEncounterScheduleForm'),
      panelEl: wildEncounterSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitWildEncounterSchedule'),
      statusEl: document.getElementById('wildEncounterScheduleStatus'),
      wildEncounterEl: wildEncounterScheduleNameEl,
      startDateEl: wildEncounterScheduleStartDateEl,
      endDateEl: wildEncounterScheduleEndDateEl,
      timeEl: wildEncounterScheduleTimeEl,
      mondayEl: wildEncounterScheduleMondayEl,
      tuesdayEl: wildEncounterScheduleTuesdayEl,
      wednesdayEl: wildEncounterScheduleWednesdayEl,
      thursdayEl: wildEncounterScheduleThursdayEl,
      fridayEl: wildEncounterScheduleFridayEl,
      saturdayEl: wildEncounterScheduleSaturdayEl,
      sundayEl: wildEncounterScheduleSundayEl,
      messageEl: document.getElementById('wildEncounterScheduleMessage'),
      activatePanel,
      hidePanels,
   });

   createEndWildEncounterScheduleController({
      showButtonEl: document.getElementById('showEndWildEncounterScheduleForm'),
      panelEl: endWildEncounterSchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitEndWildEncounterSchedule'),
      statusEl: document.getElementById('endWildEncounterScheduleStatus'),
      wildEncounterEl: endWildEncounterScheduleNameEl,
      endDateEl: endWildEncounterScheduleDateEl,
      activatePanel,
      hidePanels,
   });

   createCancelWildEncounterOccurrenceController({
      showButtonEl: document.getElementById('showCancelWildEncounterOccurrenceForm'),
      panelEl: cancelWildEncounterOccurrencePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById('submitCancelWildEncounterOccurrence'),
      statusEl: document.getElementById('cancelWildEncounterOccurrenceStatus'),
      wildEncounterEl: cancelWildEncounterOccurrenceNameEl,
      dateEl: cancelWildEncounterOccurrenceDateEl,
      timeEl: cancelWildEncounterOccurrenceTimeEl,
      activatePanel,
      hidePanels,
      occurrenceFilterController: wildEncounterOccurrenceFilterController,
   });

   initOffDisplayDatePickers(
      offDisplayStartDateEl,
      offDisplayEndDateEl
   );

   initVisibilityScheduleDateTimePickers(
      visibilityScheduleStartDateEl,
      visibilityScheduleEndDateEl,
      visibilityScheduleDailyStartTimeEl,
      visibilityScheduleDailyEndTimeEl
   );

   initOffDisplayDatePickers(
      viewingAlertStartDateEl,
      viewingAlertEndDateEl
   );

   initOffDisplayDatePickers(
      exhibitClosedStartDateEl,
      exhibitClosedEndDateEl
   );

   initOffDisplayDatePickers(
      restaurantClosedStartDateEl,
      restaurantClosedEndDateEl
   );

   initOffDisplayDatePickers(
      restaurantOpeningScheduleStartDateEl,
      restaurantOpeningScheduleEndDateEl
   );

   initOffDisplayDatePickers(
      giftShopClosedStartDateEl,
      giftShopClosedEndDateEl
   );

   initOffDisplayDatePickers(
      giftShopOpeningScheduleStartDateEl,
      giftShopOpeningScheduleEndDateEl
   );

   initOffDisplayDatePickers(
      attractionClosedStartDateEl,
      attractionClosedEndDateEl
   );

   initOffDisplayDatePickers(
      attractionOpeningScheduleStartDateEl,
      attractionOpeningScheduleEndDateEl
   );

   initOffDisplayDatePickers(
      zoomobileStationClosedStartDateEl,
      zoomobileStationClosedEndDateEl
   );

   initOffDisplayDatePickers(
      guardiansTalkScheduleStartDateEl,
      guardiansTalkScheduleEndDateEl
   );

   initOffDisplayDatePickers(
      endGuardiansTalkScheduleEndDateEl,
      null
   );

   initVisibilityScheduleDateTimePickers(
      guardiansTalkScheduleStartDateEl,
      guardiansTalkScheduleEndDateEl,
      guardiansTalkScheduleTimeEl,
      null
   );

   initOffDisplayDatePickers(
      wildEncounterScheduleStartDateEl,
      wildEncounterScheduleEndDateEl
   );

   initOffDisplayDatePickers(
      endWildEncounterScheduleDateEl,
      null
   );

   initVisibilityScheduleDateTimePickers(
      wildEncounterScheduleStartDateEl,
      wildEncounterScheduleEndDateEl,
      wildEncounterScheduleTimeEl,
      null
   );

});
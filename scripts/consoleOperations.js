import {
   initOffDisplayDatePickers,
   initVisibilityScheduleDateTimePickers
} from './ui/consoleDatePickers.js';

import { createAnimalOffDisplayController } from './consoleOperations/animals/animalOffDisplay.js';
import { createAnimalOnDisplayController } from './consoleOperations/animals/animalOnDisplay.js';
import { createAnimalVisibilityScheduleController } from './consoleOperations/animals/animalVisibilitySchedule.js';
import { createRemoveVisibilityScheduleController } from './consoleOperations/animals/removeVisibilitySchedule.js';
import { createAnimalViewingAlertController } from './consoleOperations/animals/animalViewingAlert.js';
import { createRemoveViewingAlertController } from './consoleOperations/animals/removeViewingAlert.js';

import { createExhibitClosedController } from './consoleOperations/exhibits/exhibitClosed.js';
import { createExhibitOpenController } from './consoleOperations/exhibits/exhibitOpen.js';

import { createRestaurantClosedController } from './consoleOperations/restaurants/restaurantClosed.js';
import { createRestaurantOpenController } from './consoleOperations/restaurants/restaurantOpen.js';
import { createRestaurantOpeningScheduleController } from './consoleOperations/restaurants/restaurantOpeningSchedule.js';
import { createRemoveRestaurantOpeningScheduleController } from './consoleOperations/restaurants/removeRestaurantOpeningSchedule.js';

import { createGiftShopClosedController } from './consoleOperations/giftShops/giftShopClosed.js';
import { createGiftShopOpenController } from './consoleOperations/giftShops/giftShopOpen.js';
import { createGiftShopOpeningScheduleController } from './consoleOperations/giftShops/giftShopOpeningSchedule.js';
import { createRemoveGiftShopOpeningScheduleController } from './consoleOperations/giftShops/removeGiftShopOpeningSchedule.js';

import { createAttractionClosedController } from './consoleOperations/attractions/attractionClosed.js';
import { createAttractionOpenController } from './consoleOperations/attractions/attractionOpen.js';
import { createAttractionOpeningScheduleController } from './consoleOperations/attractions/attractionOpeningSchedule.js';
import { createRemoveAttractionOpeningScheduleController } from './consoleOperations/attractions/removeAttractionOpeningSchedule.js';

import { createZoomobileRouteController } from './consoleOperations/zoomobile/zoomobileRoute.js';

import { createAnimalSpeciesAutocompleteController } from './consoleOperations/animals/animalSpeciesAutocomplete.js';

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

import { createZoomobileRoutePanelHtml } from './consoleOperations/zoomobile/panels/zoomobileRoutePanel.js';

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
      ${createZoomobileRoutePanelHtml()}
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
   const zoomobileRoutePanel = document.getElementById('zoomobileRoutePanel');

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
   const zoomobileRouteSummerEl = document.getElementById('zoomobileRouteSummer');
   const zoomobileRouteWinterEl = document.getElementById('zoomobileRouteWinter');

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

} );
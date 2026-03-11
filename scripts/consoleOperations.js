import {
   initOffDisplayDatePickers,
   initVisibilityScheduleDateTimePickers
} from './ui/consoleDatePickers.js';

import { createAnimalOffDisplayController } from './consoleOperations/animalOffDisplay.js';
import { createAnimalOnDisplayController } from './consoleOperations/animalOnDisplay.js';
import { createAnimalVisibilityScheduleController } from './consoleOperations/animalVisibilitySchedule.js';
import { createRemoveVisibilityScheduleController } from './consoleOperations/removeVisibilitySchedule.js';
import { createAnimalSpeciesAutocompleteController } from './consoleOperations/animalSpeciesAutocomplete.js';
import { createOffDisplayPanelHtml } from './consoleOperations/panels/offDisplayPanel.js';
import { createOnDisplayPanelHtml } from './consoleOperations/panels/onDisplayPanel.js';
import { createVisibilitySchedulePanelHtml } from './consoleOperations/panels/visibilitySchedulePanel.js';
import { createRemoveVisibilitySchedulePanelHtml } from './consoleOperations/panels/removeVisibilitySchedulePanel.js';

document.addEventListener( 'DOMContentLoaded', () => {

   const workspaceEl = document.getElementById( 'consoleOperationsWorkspace' );

   if ( !workspaceEl ) {
      console.warn( '[consoleOperations] missing #consoleOperationsWorkspace' );
      return;
   }

   workspaceEl.innerHTML = `
      ${createOffDisplayPanelHtml()}
      ${createOnDisplayPanelHtml()}
      ${createVisibilitySchedulePanelHtml()}
      ${createRemoveVisibilitySchedulePanelHtml()}
   `;

   const offDisplayPanel = document.getElementById( 'offDisplayPanel' );
   const onDisplayPanel = document.getElementById( 'onDisplayPanel' );
   const visibilitySchedulePanel = document.getElementById( 'visibilitySchedulePanel' );
   const removeVisibilitySchedulePanel = document.getElementById( 'removeVisibilitySchedulePanel' );

   const offDisplaySpeciesEl = document.getElementById( 'offDisplaySpecies' );
   const onDisplaySpeciesEl = document.getElementById( 'onDisplaySpecies' );
   const visibilityScheduleSpeciesEl = document.getElementById( 'visibilityScheduleSpecies' );
   const removeVisibilityScheduleSpeciesEl = document.getElementById( 'removeVisibilityScheduleSpecies' );

   const offDisplaySpeciesResults = document.getElementById( 'offDisplaySpeciesResults' );
   const onDisplaySpeciesResults = document.getElementById( 'onDisplaySpeciesResults' );
   const visibilityScheduleSpeciesResults = document.getElementById( 'visibilityScheduleSpeciesResults' );
   const removeVisibilityScheduleSpeciesResults = document.getElementById( 'removeVisibilityScheduleSpeciesResults' );

   const offDisplayExhibitEl = document.getElementById( 'offDisplayExhibit' );
   const onDisplayExhibitEl = document.getElementById( 'onDisplayExhibit' );
   const visibilityScheduleExhibitEl = document.getElementById( 'visibilityScheduleExhibit' );
   const removeVisibilityScheduleExhibitEl = document.getElementById( 'removeVisibilityScheduleExhibit' );

   const offDisplayStartDateEl = document.getElementById( 'offDisplayStartDate' );
   const offDisplayEndDateEl = document.getElementById( 'offDisplayEndDate' );

   const visibilityScheduleStartDateEl = document.getElementById( 'visibilityScheduleStartDate' );
   const visibilityScheduleEndDateEl = document.getElementById( 'visibilityScheduleEndDate' );
   const visibilityScheduleDailyStartTimeEl = document.getElementById( 'visibilityScheduleDailyStartTime' );
   const visibilityScheduleDailyEndTimeEl = document.getElementById( 'visibilityScheduleDailyEndTime' );

   function activatePanel( panelEl ) {
      document
         .querySelectorAll( '.console-operations-panel' )
         .forEach( panel => panel.classList.remove( 'active' ) );

      panelEl?.classList.add( 'active' );

      document
         .querySelectorAll( '.console-operations-menu-btn' )
         .forEach( ( button ) => {
            button.classList.toggle(
               'active',
               button.dataset.panelTarget === panelEl?.id
            );
         } );
   }

   function hidePanels() {
      document
         .querySelectorAll( '.console-operations-panel' )
         .forEach( panel => panel.classList.remove( 'active' ) );

      document
         .querySelectorAll( '.console-operations-menu-btn' )
         .forEach( button => button.classList.remove( 'active' ) );
   }

   createAnimalSpeciesAutocompleteController( {
      inputEl: offDisplaySpeciesEl,
      resultsEl: offDisplaySpeciesResults,
      exhibitEl: offDisplayExhibitEl,
   } );

   createAnimalSpeciesAutocompleteController( {
      inputEl: onDisplaySpeciesEl,
      resultsEl: onDisplaySpeciesResults,
      exhibitEl: onDisplayExhibitEl,
   } );

   createAnimalSpeciesAutocompleteController( {
      inputEl: visibilityScheduleSpeciesEl,
      resultsEl: visibilityScheduleSpeciesResults,
      exhibitEl: visibilityScheduleExhibitEl,
   } );

   createAnimalSpeciesAutocompleteController( {
      inputEl: removeVisibilityScheduleSpeciesEl,
      resultsEl: removeVisibilityScheduleSpeciesResults,
      exhibitEl: removeVisibilityScheduleExhibitEl,
   } );

   createAnimalOffDisplayController( {
      showButtonEl: document.getElementById( 'showOffDisplayForm' ),
      panelEl: offDisplayPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById( 'submitOffDisplay' ),
      statusEl: document.getElementById( 'offDisplayStatus' ),
      speciesEl: offDisplaySpeciesEl,
      exhibitEl: offDisplayExhibitEl,
      startDateEl: offDisplayStartDateEl,
      endDateEl: offDisplayEndDateEl,
      messageEl: document.getElementById( 'offDisplayMessage' ),
      activatePanel,
      hidePanels,
   } );

   createAnimalOnDisplayController( {
      showButtonEl: document.getElementById( 'showOnDisplayForm' ),
      panelEl: onDisplayPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById( 'submitOnDisplay' ),
      statusEl: document.getElementById( 'onDisplayStatus' ),
      speciesEl: onDisplaySpeciesEl,
      exhibitEl: onDisplayExhibitEl,
      activatePanel,
      hidePanels,
   } );

   createAnimalVisibilityScheduleController( {
      showButtonEl: document.getElementById( 'showVisibilityScheduleForm' ),
      panelEl: visibilitySchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById( 'submitVisibilitySchedule' ),
      statusEl: document.getElementById( 'visibilityScheduleStatus' ),
      speciesEl: visibilityScheduleSpeciesEl,
      exhibitEl: visibilityScheduleExhibitEl,
      startDateEl: visibilityScheduleStartDateEl,
      endDateEl: visibilityScheduleEndDateEl,
      dailyStartTimeEl: visibilityScheduleDailyStartTimeEl,
      dailyEndTimeEl: visibilityScheduleDailyEndTimeEl,
      messageEl: document.getElementById( 'visibilityScheduleMessage' ),
      activatePanel,
      hidePanels,
   } );

   createRemoveVisibilityScheduleController( {
      showButtonEl: document.getElementById( 'showRemoveVisibilityScheduleForm' ),
      panelEl: removeVisibilitySchedulePanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById( 'submitRemoveVisibilitySchedule' ),
      statusEl: document.getElementById( 'removeVisibilityScheduleStatus' ),
      speciesEl: removeVisibilityScheduleSpeciesEl,
      exhibitEl: removeVisibilityScheduleExhibitEl,
      activatePanel,
      hidePanels,
   } );

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

} );
import { initFlatpickr } from './ui/flatpickr.js';
import { createAnimalOffDisplayController } from './consoleOperations/animalOffDisplay.js';
import { createAnimalOnDisplayController } from './consoleOperations/animalOnDisplay.js';
import { createAnimalVisibilityScheduleController } from './consoleOperations/animalVisibilitySchedule.js';
import { createAnimalSpeciesAutocompleteController } from './consoleOperations/animalSpeciesAutocomplete.js';
import { createOffDisplayPanelHtml } from './consoleOperations/panels/offDisplayPanel.js';
import { createOnDisplayPanelHtml } from './consoleOperations/panels/onDisplayPanel.js';
import { createVisibilitySchedulePanelHtml } from './consoleOperations/panels/visibilitySchedulePanel.js';

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
   `;

   const offDisplayPanel = document.getElementById( 'offDisplayPanel' );
   const onDisplayPanel = document.getElementById( 'onDisplayPanel' );
   const visibilitySchedulePanel = document.getElementById( 'visibilitySchedulePanel' );

   const offDisplaySpeciesEl = document.getElementById( 'offDisplaySpecies' );
   const onDisplaySpeciesEl = document.getElementById( 'onDisplaySpecies' );
   const visibilityScheduleSpeciesEl = document.getElementById( 'visibilityScheduleSpecies' );

   const offDisplaySpeciesResults = document.getElementById( 'offDisplaySpeciesResults' );
   const onDisplaySpeciesResults = document.getElementById( 'onDisplaySpeciesResults' );
   const visibilityScheduleSpeciesResults = document.getElementById( 'visibilityScheduleSpeciesResults' );

   const offDisplayExhibitEl = document.getElementById( 'offDisplayExhibit' );
   const onDisplayExhibitEl = document.getElementById( 'onDisplayExhibit' );
   const visibilityScheduleExhibitEl = document.getElementById( 'visibilityScheduleExhibit' );

   const offDisplayStartTimeEl = document.getElementById( 'offDisplayStartTime' );
   const offDisplayEndTimeEl = document.getElementById( 'offDisplayEndTime' );

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

   function initOffDisplayDateTimePickers() {
      function applyFutureConstraint( picker ) {
         if ( !picker ) return;

         const now = new Date();
         const selectedDate = picker.selectedDates?.[0] ?? null;

         if ( selectedDate ) {
            const isToday =
               selectedDate.getFullYear() === now.getFullYear()
               && selectedDate.getMonth() === now.getMonth()
               && selectedDate.getDate() === now.getDate();

            if ( isToday ) {
               picker.set( 'minTime', now );
            } else {
               picker.set( 'minTime', null );
            }
         } else {
            picker.set( 'minTime', now );
         }
      }

      const startPicker = initFlatpickr( offDisplayStartTimeEl, {
         enableTime: true,
         dateFormat: 'Y-m-d h:i K',
         time_24hr: false,
         minDate: 'today',
         defaultHour: new Date().getHours(),
         defaultMinute: new Date().getMinutes(),
         onOpen: [ ( _, __, fp ) => applyFutureConstraint( fp ) ],
         onChange: [ ( _, __, fp ) => applyFutureConstraint( fp ) ]
      } );

      const endPicker = initFlatpickr( offDisplayEndTimeEl, {
         enableTime: true,
         dateFormat: 'Y-m-d h:i K',
         time_24hr: false,
         minDate: 'today',
         defaultHour: new Date().getHours(),
         defaultMinute: new Date().getMinutes(),
         onOpen: [ ( _, __, fp ) => applyFutureConstraint( fp ) ],
         onChange: [ ( _, __, fp ) => applyFutureConstraint( fp ) ]
      } );

      if ( offDisplayStartTimeEl && endPicker ) {
         offDisplayStartTimeEl.addEventListener( 'change', () => {
            const startValue = offDisplayStartTimeEl.value?.trim();

            if ( startValue ) {
               endPicker.set( 'minDate', startValue );

               const startDate = new Date( startValue );
               const now = new Date();

               const sameDayAsToday =
                  startDate.getFullYear() === now.getFullYear()
                  && startDate.getMonth() === now.getMonth()
                  && startDate.getDate() === now.getDate();

               if ( sameDayAsToday ) {
                  endPicker.set( 'minTime', now );
               } else {
                  endPicker.set( 'minTime', null );
               }
            } else {
               endPicker.set( 'minDate', 'today' );
               endPicker.set( 'minTime', new Date() );
            }
         } );
      }

      return { startPicker, endPicker };
   }

   function initVisibilityScheduleDateTimePickers() {
      const startDatePicker = initFlatpickr( visibilityScheduleStartDateEl, {
         enableTime: false,
         dateFormat: 'Y-m-d'
      } );

      const endDatePicker = initFlatpickr( visibilityScheduleEndDateEl, {
         enableTime: false,
         dateFormat: 'Y-m-d'
      } );

      const dailyStartTimePicker = initFlatpickr( visibilityScheduleDailyStartTimeEl, {
         enableTime: true,
         noCalendar: true,
         dateFormat: 'h:i K',
         time_24hr: false
      } );

      const dailyEndTimePicker = initFlatpickr( visibilityScheduleDailyEndTimeEl, {
         enableTime: true,
         noCalendar: true,
         dateFormat: 'h:i K',
         time_24hr: false
      } );

      if ( visibilityScheduleStartDateEl && endDatePicker ) {
         visibilityScheduleStartDateEl.addEventListener( 'change', () => {
            const startValue = visibilityScheduleStartDateEl.value?.trim();

            if ( startValue ) {
               endDatePicker.set( 'minDate', startValue );
            } else {
               endDatePicker.set( 'minDate', null );
            }
         } );
      }

      return {
         startDatePicker,
         endDatePicker,
         dailyStartTimePicker,
         dailyEndTimePicker
      };
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

   createAnimalOffDisplayController( {
      showButtonEl: document.getElementById( 'showOffDisplayForm' ),
      panelEl: offDisplayPanel,
      cancelButtonEl: null,
      submitButtonEl: document.getElementById( 'submitOffDisplay' ),
      statusEl: document.getElementById( 'offDisplayStatus' ),
      speciesEl: offDisplaySpeciesEl,
      exhibitEl: offDisplayExhibitEl,
      startTimeEl: offDisplayStartTimeEl,
      endTimeEl: offDisplayEndTimeEl,
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

   initOffDisplayDateTimePickers();
   initVisibilityScheduleDateTimePickers();

} );
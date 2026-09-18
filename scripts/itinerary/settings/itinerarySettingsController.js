import { ItineraryService } from '../itineraryService.js';
import { ItinerarySettingsFragment } from './itinerarySettingsFragment.js';
import { ItinerarySettingsPreferenceDiff } from './itinerarySettingsPreferenceDiff.js';
import { ItinerarySettingsWarningCopy } from './itinerarySettingsWarningCopy.js';
import { ConfirmFragment } from '../panel/components/confirmFragment.js';
import { ItineraryPanelFragment } from '../panel/components/itineraryPanelFragment.js';
import { PersistItineraryWarningSuppressor } from '../persistItineraryWarningSuppressor.js';
import { Strings } from '../../strings.js';

export class ItinerarySettingsController {
   static createItinerarySettingsController({
      gearEl,
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl(),
      loadItinerary = ItineraryService.getItinerary,
      persistSuppression = PersistItineraryWarningSuppressor.persistItineraryWarningSuppression,
      persistUnsuppression = PersistItineraryWarningSuppressor.persistItineraryWarningUnsuppression,
      showOverlay = ItinerarySettingsFragment.showItinerarySettingsOverlay,
      showConfirmPopup = ConfirmFragment.showItineraryConfirmPopup,
   } = {}) {
      async function persistChanges(changes) {
         for (const change of changes) {
            if (change.showWarning) {
               await persistUnsuppression(change.status);
            }
            else {
               await persistSuppression(change.status);
            }
         }
      }

      async function saveAndClose(changes, close) {
         try {
            await persistChanges(changes);
            close();
         }
         catch {
         }
      }

      function handleClose(statuses, { close, view }) {
         const changes = ItinerarySettingsPreferenceDiff.changesFromCheckboxes(
            statuses,
            view.checkboxEls
         );

         if (!changes.length) {
            close();
            return;
         }

         showConfirmPopup({
            title: Strings.itinerary.confirmation.saveChangesTitle,
            message: Strings.itinerary.settings.saveChangesMessage,
            confirmText: Strings.actions.save,
            cancelText: Strings.itinerary.actions.discard,
            onConfirm: () => saveAndClose(changes, close),
            onCancel: close,
         });
      }

      async function open() {
         let statuses = [];

         try {
            const itinerary = await loadItinerary();
            statuses = ItinerarySettingsWarningCopy.suppressableStatuses(
               itinerary?.itineraryConfig
            );
         }
         catch {
            statuses = [];
         }

         showOverlay({
            mountEl,
            statuses,
            onSave: ({ close, view }) => {
               const changes = ItinerarySettingsPreferenceDiff.changesFromCheckboxes(
                  statuses,
                  view.checkboxEls
               );

               return saveAndClose(changes, close);
            },
            onClose: (args) => {
               handleClose(statuses, args);
            },
         });
      }

      if (gearEl) {
         gearEl.addEventListener('click', () => open());
      }

      return {
         open,
      };
   }
}

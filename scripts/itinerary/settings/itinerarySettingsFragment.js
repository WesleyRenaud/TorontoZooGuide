import { ItineraryCardModal } from '../itineraryCardModal.js';
import { ItinerarySettingsView } from './itinerarySettingsView.js';
import { ItineraryPanelFragment } from '../panel/components/itineraryPanelFragment.js';

export class ItinerarySettingsFragment {
   static SETTINGS_OVERLAY_SELECTOR = '.itin-settings-overlay';

   static showItinerarySettingsOverlay({
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl() ?? document.body,
      statuses = [],
      onSave = null,
      onClose = null,
   } = {}) {
      const existingOverlay = mountEl.querySelector?.(
         ItinerarySettingsFragment.SETTINGS_OVERLAY_SELECTOR
      ) ?? document.querySelector(ItinerarySettingsFragment.SETTINGS_OVERLAY_SELECTOR);
      existingOverlay?.__tzgPopupCleanup?.();
      existingOverlay?.remove();
      ItineraryCardModal.release();

      const view = ItinerarySettingsView.buildItinerarySettingsView({
         statuses,
      });

      const popup = ItineraryPanelFragment.mountDismissablePopup({
         mountEl,
         root: view.root,
         overlay: view.root,
         initialFocusEl: null,
         dismissOnOverlayClick: false,
         dismissOnEscape: false,
      });

      function closeOverlay() {
         ItineraryCardModal.release();
         popup.close();
      }

      ItineraryCardModal.syncOpenCard(mountEl, {
         returnFocusFallback: ItineraryCardModal.getGearButton(),
         onEscape: () => {
            view.closeButtonEl.click();
         },
      });

      view.closeButtonEl.addEventListener('click', () => {
         if (onClose) {
            onClose({ close: closeOverlay, view });
            return;
         }

         closeOverlay();
      });

      view.saveButtonEl.addEventListener('click', () => {
         if (onSave) {
            onSave({ close: closeOverlay, view });
            return;
         }

         closeOverlay();
      });

      return view;
   }
}

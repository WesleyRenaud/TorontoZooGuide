import { OverlayModal } from '../overlays/overlayModal.js';

export class ItineraryCardModal {
   static TITLE_ID = 'itineraryCardTitle';
   static CARD_SELECTOR = '.itin-card';
   static HEADING_SELECTOR = '.itin-h1';
   static BUILD_BUTTON_SELECTOR = '.itin-panel-build-btn';
   static GEAR_BUTTON_ID = 'itinerarySettingsGear';
   static NESTED_POPUP_SELECTOR = '.tzg-popup';
   static DATE_PICKER_SELECTOR = '.flatpickr-calendar';
   static POINTER_OPENED_ATTRIBUTE = OverlayModal.POINTER_OPENED_ATTRIBUTE;

   static modal = null;
   static mountEl = null;
   static onEscape = null;
   static installedDocument = null;

   static getBuildItineraryButton() {
      return globalThis.document?.querySelector(ItineraryCardModal.BUILD_BUTTON_SELECTOR)
         ?? null;
   }

   static getGearButton() {
      return globalThis.document?.getElementById(ItineraryCardModal.GEAR_BUTTON_ID)
         ?? null;
   }

   static getTopCard(mountEl = ItineraryCardModal.mountEl) {
      if (!mountEl) {
         return null;
      }

      const nestedPopup = mountEl.querySelector(ItineraryCardModal.NESTED_POPUP_SELECTOR);
      const nestedCard = nestedPopup?.querySelector(ItineraryCardModal.CARD_SELECTOR);

      if (nestedCard) {
         return nestedCard;
      }

      return mountEl.querySelector(ItineraryCardModal.CARD_SELECTOR);
   }

   static getTitle(dialog) {
      return dialog?.querySelector(ItineraryCardModal.HEADING_SELECTOR) ?? null;
   }

   static hasOpenDatePicker() {
      const calendars = globalThis.document?.querySelectorAll?.(
         ItineraryCardModal.DATE_PICKER_SELECTOR
      ) ?? [];

      for (const calendar of calendars) {
         if (calendar.classList?.contains('open')) {
            return true;
         }
      }

      return false;
   }

   static hasNestedPopup() {
      return Boolean(
         ItineraryCardModal.mountEl?.querySelector(ItineraryCardModal.NESTED_POPUP_SELECTOR)
      );
   }

   static ensureModal() {
      if (!ItineraryCardModal.modal) {
         ItineraryCardModal.modal = OverlayModal.createOverlayModal({
            getOverlay: () => ItineraryCardModal.mountEl,
            getDialog: () => ItineraryCardModal.getTopCard(),
            getTitle: ItineraryCardModal.getTitle,
            titleId: ItineraryCardModal.TITLE_ID,
         });
      }

      const doc = globalThis.document;

      if (ItineraryCardModal.installedDocument === doc) {
         return ItineraryCardModal.modal;
      }

      if (ItineraryCardModal.modal.isActive()) {
         ItineraryCardModal.modal.deactivate();
      }

      ItineraryCardModal.modal.install();
      doc?.addEventListener?.(
         'keydown',
         ItineraryCardModal.handleDocumentKeydown,
         true
      );
      ItineraryCardModal.installedDocument = doc ?? null;

      return ItineraryCardModal.modal;
   }

   static handleDocumentKeydown(event) {
      const modal = ItineraryCardModal.modal;

      if (!modal) {
         return;
      }

      modal.handleKeydown(event);
      ItineraryCardModal.handleEscape(event);
   }

   static handleEscape(event) {
      if (event.key !== 'Escape') {
         return;
      }

      if (!ItineraryCardModal.modal?.isActive()) {
         return;
      }

      if (event.defaultPrevented) {
         return;
      }

      if (ItineraryCardModal.hasOpenDatePicker()) {
         return;
      }

      if (ItineraryCardModal.hasNestedPopup()) {
         return;
      }

      const onEscape = ItineraryCardModal.onEscape;

      if (!onEscape) {
         return;
      }

      event.preventDefault();
      event.stopPropagation();
      onEscape();
   }

   static syncOpenCard(mountEl, { returnFocusFallback = null, onEscape = null } = {}) {
      if (!mountEl) {
         return;
      }

      ItineraryCardModal.mountEl = mountEl;
      ItineraryCardModal.onEscape = onEscape;

      const modal = ItineraryCardModal.ensureModal();

      if (modal.isActive()) {
         modal.refresh();
         return;
      }

      modal.activate({
         returnFocusFallback: returnFocusFallback
            ?? ItineraryCardModal.getBuildItineraryButton(),
      });
   }

   static release() {
      if (!ItineraryCardModal.modal) {
         return;
      }

      ItineraryCardModal.modal.deactivate();
      ItineraryCardModal.onEscape = null;
      ItineraryCardModal.mountEl = null;
   }
}

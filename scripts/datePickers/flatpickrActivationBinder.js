export class FlatpickrActivationBinder {
   static HAS_POPUP_VALUE = 'dialog';
   static EXPANDED_TRUE = 'true';
   static EXPANDED_FALSE = 'false';
   static ENTER_KEY = 'Enter';
   static SPACE_KEY = ' ';
   static ARROW_DOWN_KEY = 'ArrowDown';
   static OPEN_KEYS = new Set([
      FlatpickrActivationBinder.ENTER_KEY,
      FlatpickrActivationBinder.SPACE_KEY,
      FlatpickrActivationBinder.ARROW_DOWN_KEY,
   ]);
   static SELECTED_DAY_SELECTOR = '.flatpickr-day.selected';
   static TODAY_DAY_SELECTOR = '.flatpickr-day.today';
   static HOUR_SELECTOR = '.flatpickr-hour';
   static ENABLED_DAY_SELECTOR = '.flatpickr-day:not(.hidden):not(.flatpickr-disabled)';
   static CALENDAR_ID_PREFIX = 'tzg-flatpickr-';
   static INSTALLED_PROPERTY = '__tzgPickerActivationBound';
   static POINTER_OPENED_PROPERTY = '__tzgPickerOpenedByPointer';
   static nextCalendarId = 1;

   static isOpenKey(key) {
      return FlatpickrActivationBinder.OPEN_KEYS.has(key);
   }

   static wasOpenedByPointer(inputEl) {
      return Boolean(inputEl?.[FlatpickrActivationBinder.POINTER_OPENED_PROPERTY]);
   }

   static install(inputEl, getInstance) {
      if (!inputEl || typeof getInstance !== 'function') {
         return;
      }

      if (inputEl[FlatpickrActivationBinder.INSTALLED_PROPERTY]) {
         return;
      }

      inputEl[FlatpickrActivationBinder.INSTALLED_PROPERTY] = true;
      inputEl[FlatpickrActivationBinder.POINTER_OPENED_PROPERTY] = false;
      FlatpickrActivationBinder.decorateInput(inputEl, getInstance());
      FlatpickrActivationBinder.hookInstanceLifecycle(getInstance(), {
         onOpen() {
            FlatpickrActivationBinder.syncExpanded(inputEl, true);
            FlatpickrActivationBinder.decorateInput(inputEl, getInstance());
         },
         onClose() {
            FlatpickrActivationBinder.syncExpanded(inputEl, false);

            if (FlatpickrActivationBinder.wasOpenedByPointer(inputEl)) {
               return;
            }

            FlatpickrActivationBinder.restoreFocusToInput(inputEl, getInstance());
         },
      });

      inputEl.addEventListener('mousedown', (event) => {
         FlatpickrActivationBinder.handlePointerActivation(event, inputEl, getInstance);
      });
      inputEl.addEventListener('keydown', (event) => {
         FlatpickrActivationBinder.handleKeyboardActivation(event, inputEl, getInstance);
      });
   }

   static decorateInput(inputEl, instance) {
      if (!inputEl) {
         return;
      }

      inputEl.setAttribute('aria-haspopup', FlatpickrActivationBinder.HAS_POPUP_VALUE);
      FlatpickrActivationBinder.syncExpanded(
         inputEl,
         Boolean(instance?.isOpen)
      );

      const calendarId = FlatpickrActivationBinder.ensureCalendarId(instance);

      if (!calendarId) {
         return;
      }

      inputEl.setAttribute('aria-controls', calendarId);
   }

   static syncExpanded(inputEl, isOpen) {
      if (!inputEl) {
         return;
      }

      if (isOpen) {
         inputEl.setAttribute('aria-expanded', FlatpickrActivationBinder.EXPANDED_TRUE);
         return;
      }

      inputEl.setAttribute('aria-expanded', FlatpickrActivationBinder.EXPANDED_FALSE);
   }

   static ensureCalendarId(instance) {
      const calendar = instance?.calendarContainer;

      if (!calendar) {
         return null;
      }

      if (!calendar.id) {
         calendar.id = (
            `${FlatpickrActivationBinder.CALENDAR_ID_PREFIX}`
            + `${FlatpickrActivationBinder.nextCalendarId}`
         );
         FlatpickrActivationBinder.nextCalendarId += 1;
      }

      return calendar.id;
   }

   static hookInstanceLifecycle(instance, { onOpen, onClose } = {}) {
      if (!instance?.config) {
         return;
      }

      FlatpickrActivationBinder.appendHook(instance, 'onOpen', onOpen);
      FlatpickrActivationBinder.appendHook(instance, 'onClose', onClose);
   }

   static appendHook(instance, hookName, handler) {
      if (!handler) {
         return;
      }

      const existing = instance.config[hookName];

      if (Array.isArray(existing)) {
         existing.push(handler);
         return;
      }

      if (typeof existing === 'function') {
         instance.config[hookName] = [existing, handler];
         return;
      }

      instance.config[hookName] = [handler];
   }

   static canActivate(inputEl) {
      return Boolean(inputEl) && !inputEl.disabled;
   }

   static handlePointerActivation(event, inputEl, getInstance) {
      if (event?.button && event.button !== 0) {
         return;
      }

      if (!FlatpickrActivationBinder.canActivate(inputEl)) {
         return;
      }

      const instance = getInstance();

      if (!instance || instance.isOpen) {
         return;
      }

      inputEl[FlatpickrActivationBinder.POINTER_OPENED_PROPERTY] = true;
      instance.open();
      FlatpickrActivationBinder.syncExpanded(inputEl, true);
   }

   static handleKeyboardActivation(event, inputEl, getInstance) {
      if (!FlatpickrActivationBinder.canActivate(inputEl)) {
         return;
      }

      if (event.altKey || event.ctrlKey || event.metaKey) {
         return;
      }

      if (!FlatpickrActivationBinder.isOpenKey(event.key)) {
         return;
      }

      const instance = getInstance();

      if (!instance || instance.isOpen) {
         return;
      }

      event.preventDefault();
      event.stopPropagation();
      inputEl[FlatpickrActivationBinder.POINTER_OPENED_PROPERTY] = false;
      instance.open();
      FlatpickrActivationBinder.syncExpanded(inputEl, true);
      FlatpickrActivationBinder.focusInsidePicker(instance);
   }

   static getInitialPickerFocus(instance) {
      if (instance?.selectedDateElem) {
         return instance.selectedDateElem;
      }

      if (instance?.todayDateElem) {
         return instance.todayDateElem;
      }

      const calendar = instance?.calendarContainer;

      if (!calendar?.querySelector) {
         return instance?.hourElement ?? null;
      }

      const selected = calendar.querySelector(
         FlatpickrActivationBinder.SELECTED_DAY_SELECTOR
      );

      if (selected) {
         return selected;
      }

      const today = calendar.querySelector(
         FlatpickrActivationBinder.TODAY_DAY_SELECTOR
      );

      if (today) {
         return today;
      }

      if (instance?.hourElement) {
         return instance.hourElement;
      }

      const hour = calendar.querySelector(FlatpickrActivationBinder.HOUR_SELECTOR);

      if (hour) {
         return hour;
      }

      return calendar.querySelector(FlatpickrActivationBinder.ENABLED_DAY_SELECTOR);
   }

   static focusInsidePicker(instance) {
      const target = FlatpickrActivationBinder.getInitialPickerFocus(instance);
      target?.focus?.();
   }

   static isFocusInsidePicker(activeElement, instance) {
      const calendar = instance?.calendarContainer;

      if (!calendar?.contains || !activeElement) {
         return false;
      }

      return calendar.contains(activeElement);
   }

   static shouldRestoreFocus(inputEl, instance) {
      if (!inputEl || typeof document === 'undefined') {
         return false;
      }

      const activeElement = document.activeElement;

      if (!activeElement) {
         return true;
      }

      if (activeElement === inputEl) {
         return false;
      }

      if (
         activeElement === document.body
         || activeElement === document.documentElement
      ) {
         return true;
      }

      return FlatpickrActivationBinder.isFocusInsidePicker(activeElement, instance);
   }

   static restoreFocusToInput(inputEl, instance) {
      if (!FlatpickrActivationBinder.shouldRestoreFocus(inputEl, instance)) {
         return;
      }

      inputEl.focus?.();
   }
}

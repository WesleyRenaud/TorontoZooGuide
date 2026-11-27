export class TooltipFocusManager {
   static isHiddenElement(element) {
      return Boolean(element?.hidden) || element?.style?.display === 'none';
   }

   static isFocusableElement(element) {
      if (!element || typeof element.focus !== 'function' || element.disabled) {
         return false;
      }

      const tabIndex = element.getAttribute?.('tabindex');

      if (tabIndex != null && Number(tabIndex) < 0) {
         return false;
      }

      const tagName = String(element.tagName || '').toLowerCase();

      if (tagName === 'button'
         || tagName === 'input'
         || tagName === 'select'
         || tagName === 'textarea') {
         return true;
      }

      if (tagName === 'a' && element.getAttribute?.('href')) {
         return true;
      }

      return tabIndex != null && Number(tabIndex) >= 0;
   }

   static collectFocusableElements(rootEl) {
      const found = [];

      function walk(element) {
         Array.from(element?.children ?? []).forEach((child) => {
            if (!child || typeof child !== 'object' || TooltipFocusManager.isHiddenElement(child)) {
               return;
            }

            if (TooltipFocusManager.isFocusableElement(child)) {
               found.push(child);
            }

            walk(child);
         });
      }

      walk(rootEl);

      return found;
   }

   static POINTER_OPENED_ATTRIBUTE = 'data-pointer-opened';

   static focusElement(element, { pointer = false } = {}) {
      const options = pointer
         ? { preventScroll: true, focusVisible: false }
         : { preventScroll: true };

      element?.focus?.(options);
   }

   static createTooltipFocusManager({
      tooltipEl,
      getOpener,
      isOpen,
      onFocusLeave,
      isFocusLeaveSuspended = () => false,
      getBannerFocusables = () => [],
   }) {
      let installed = false;

      function getActiveElement() {
         return globalThis.document?.activeElement ?? null;
      }

      function isBannerElement(element) {
         return getBannerFocusables().includes(element);
      }

      function findBannerCloseButton() {
         const bannerFocusables = getBannerFocusables();

         if (bannerFocusables.length === 0) {
            return null;
         }

         return bannerFocusables[0];
      }

      function isTooltipDescendant(element) {
         if (!tooltipEl || typeof tooltipEl.contains !== 'function') {
            return false;
         }

         return Boolean(tooltipEl.contains(element));
      }

      function containsFocus() {
         const active = getActiveElement();

         if (!active) {
            return false;
         }

         if (isBannerElement(active)) {
            return true;
         }

         return isTooltipDescendant(active);
      }

      function getFocusableElements() {
         return TooltipFocusManager.collectFocusableElements(tooltipEl);
      }

      function getInitialFocusTarget() {
         const focusable = getFocusableElements();
         const firstCardLink = focusable.find((element) => (
            !element.classList?.contains?.('tooltip-arrow')
            && !element.classList?.contains?.('tooltip-close')
         ));

         return firstCardLink || focusable[0] || tooltipEl;
      }

      function setPointerOpened(isPointerOpened) {
         if (isPointerOpened) {
            tooltipEl?.setAttribute?.(TooltipFocusManager.POINTER_OPENED_ATTRIBUTE, '');
            return;
         }

         tooltipEl?.removeAttribute?.(TooltipFocusManager.POINTER_OPENED_ATTRIBUTE);
      }

      function focusInitial({ pointer = false } = {}) {
         setPointerOpened(pointer);
         TooltipFocusManager.focusElement(getInitialFocusTarget(), { pointer });
      }

      function clearPointerOpened() {
         setPointerOpened(false);
      }

      function recoverFocus() {
         if (!containsFocus()) {
            return;
         }

         const active = getActiveElement();

         if (active === tooltipEl) {
            return;
         }

         if (isBannerElement(active)) {
            return;
         }

         if (getFocusableElements().includes(active)) {
            return;
         }

         focusInitial();
      }

      function isPointerOpened() {
         return Boolean(tooltipEl?.hasAttribute?.(TooltipFocusManager.POINTER_OPENED_ATTRIBUTE));
      }

      function restoreFocusToOpener() {
         TooltipFocusManager.focusElement(getOpener(), { pointer: isPointerOpened() });
      }

      function handleTab(event) {
         if (event.key !== 'Tab' || event.altKey || event.ctrlKey || event.metaKey) {
            return;
         }

         const opener = getOpener();

         if (!opener) {
            return;
         }

         const focusable = getFocusableElements();
         const active = getActiveElement();

         if (isBannerElement(active)) {
            handleBannerTab(event, opener, focusable);
            return;
         }

         const isFirst = active === tooltipEl || active === focusable[0];
         const isLast = active === tooltipEl
            ? focusable.length === 0
            : active === focusable[focusable.length - 1];

         if (event.shiftKey && isFirst) {
            event.preventDefault();
            TooltipFocusManager.focusElement(opener);
            return;
         }

         if (event.shiftKey || !isLast) {
            return;
         }

         const bannerCloseButton = findBannerCloseButton();

         if (bannerCloseButton) {
            event.preventDefault();
            TooltipFocusManager.focusElement(bannerCloseButton);
            return;
         }

         TooltipFocusManager.focusElement(opener);
      }

      function handleBannerTab(event, opener, focusable) {
         if (!event.shiftKey) {
            TooltipFocusManager.focusElement(opener);
            return;
         }

         event.preventDefault();

         if (focusable.length === 0) {
            TooltipFocusManager.focusElement(tooltipEl);
            return;
         }

         TooltipFocusManager.focusElement(focusable[focusable.length - 1]);
      }

      function handleKeydown(event) {
         clearPointerOpened();
         handleTab(event);
      }

      function handleBannerKeydown(event) {
         if (!isBannerElement(event.target)) {
            return;
         }

         clearPointerOpened();
         handleTab(event);
      }

      function handleBannerFocusOut(event) {
         if (!isBannerElement(event.target)) {
            return;
         }

         handleFocusOut();
      }

      function handleFocusOut() {
         setTimeout(() => {
            if (!isOpen() || isFocusLeaveSuspended()) {
               return;
            }

            if (typeof globalThis.document?.hasFocus === 'function' && !globalThis.document.hasFocus()) {
               return;
            }

            const active = getActiveElement();

            if (!active || active === globalThis.document?.body) {
               return;
            }

            if (isTooltipDescendant(active)) {
               return;
            }

            if (isBannerElement(active)) {
               return;
            }

            if (active === getOpener()) {
               return;
            }

            onFocusLeave?.();
         }, 0);
      }

      function install() {
         if (installed || !tooltipEl) {
            return;
         }

         installed = true;
         tooltipEl.setAttribute('role', 'dialog');
         tooltipEl.setAttribute('tabindex', '-1');
         tooltipEl.addEventListener('keydown', handleKeydown);
         tooltipEl.addEventListener('focusout', handleFocusOut);
         document.addEventListener('keydown', handleBannerKeydown);
         document.addEventListener('focusout', handleBannerFocusOut);
      }

      return {
         install,
         containsFocus,
         focusInitial,
         clearPointerOpened,
         recoverFocus,
         restoreFocusToOpener,
         getFocusableElements,
         handleTab,
         handleFocusOut,
      };
   }
}

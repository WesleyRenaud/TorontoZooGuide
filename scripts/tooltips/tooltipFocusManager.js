export class TooltipFocusManager {
   static isHiddenElement(element) {
      return Boolean(element?.hidden) || element?.style?.display === 'none';
   }

   static isFocusableElement(element) {
      if (!element || typeof element.focus !== 'function' || element.disabled) {
         return false;
      }

      const tagName = String(element.tagName || '').toLowerCase();

      if (tagName === 'button') {
         return true;
      }

      if (tagName === 'a' && element.getAttribute?.('href')) {
         return true;
      }

      const tabIndex = element.getAttribute?.('tabindex');

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

   static focusElement(element) {
      element?.focus?.({ preventScroll: true });
   }

   static createTooltipFocusManager({
      tooltipEl,
      getOpener,
      isOpen,
      onFocusLeave,
   }) {
      let installed = false;

      function getActiveElement() {
         return globalThis.document?.activeElement ?? null;
      }

      function containsFocus() {
         const active = getActiveElement();

         return Boolean(active && tooltipEl?.contains?.(active));
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

      function focusInitial() {
         TooltipFocusManager.focusElement(getInitialFocusTarget());
      }

      function recoverFocus() {
         if (!containsFocus()) {
            return;
         }

         const active = getActiveElement();

         if (active === tooltipEl || getFocusableElements().includes(active)) {
            return;
         }

         focusInitial();
      }

      function restoreFocusToOpener() {
         TooltipFocusManager.focusElement(getOpener());
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
         const isFirst = active === tooltipEl || active === focusable[0];
         const isLast = active === tooltipEl
            ? focusable.length === 0
            : active === focusable[focusable.length - 1];

         if (event.shiftKey && isFirst) {
            event.preventDefault();
            TooltipFocusManager.focusElement(opener);
            return;
         }

         if (!event.shiftKey && isLast) {
            TooltipFocusManager.focusElement(opener);
         }
      }

      function handleFocusOut() {
         setTimeout(() => {
            if (!isOpen()) {
               return;
            }

            if (typeof globalThis.document?.hasFocus === 'function' && !globalThis.document.hasFocus()) {
               return;
            }

            const active = getActiveElement();

            if (!active || active === globalThis.document?.body) {
               return;
            }

            if (tooltipEl?.contains?.(active) || active === getOpener()) {
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
         tooltipEl.addEventListener('keydown', handleTab);
         tooltipEl.addEventListener('focusout', handleFocusOut);
      }

      return {
         install,
         containsFocus,
         focusInitial,
         recoverFocus,
         restoreFocusToOpener,
         getFocusableElements,
         handleTab,
         handleFocusOut,
      };
   }
}

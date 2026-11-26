import { TooltipFocusManager } from '../tooltips/tooltipFocusManager.js';

export class OverlayModal {
   static POINTER_OPENED_ATTRIBUTE = 'data-pointer-opened';
   static NON_CONTENT_TAGS = new Set(['script', 'style', 'link', 'template', 'noscript']);
   static RELATED_POPUP_SELECTOR = '.flatpickr-calendar';

   static createOverlayModal({
      getOverlay,
      getDialog,
      getTitle = OverlayModal.getDefaultTitle,
      titleId = null,
      decorateDialog = OverlayModal.decorateNothing,
   } = {}) {
      let isActive = false;
      let lastInputWasPointer = false;
      let returnFocusEl = null;
      let returnFocusFallbackEl = null;
      let inertedElements = [];

      function getActiveElement() {
         return globalThis.document?.activeElement ?? null;
      }

      function isFocusLost(element = getActiveElement()) {
         return !element || element === globalThis.document?.body;
      }

      function isRelatedFocusTarget(element) {
         return Boolean(element?.closest?.(OverlayModal.RELATED_POPUP_SELECTOR));
      }

      function isInsideInertElement(element) {
         let node = element;

         while (node) {
            if (node.hasAttribute?.('inert')) {
               return true;
            }

            node = node.parentElement;
         }

         return false;
      }

      function canReturnFocusTo(element) {
         return Boolean(element)
            && element.isConnected !== false
            && !isInsideInertElement(element);
      }

      function getReturnFocusTarget() {
         if (canReturnFocusTo(returnFocusEl)) {
            return returnFocusEl;
         }

         if (canReturnFocusTo(returnFocusFallbackEl)) {
            return returnFocusFallbackEl;
         }

         return null;
      }

      function moveFocus(element) {
         TooltipFocusManager.focusElement(element, { pointer: lastInputWasPointer });
      }

      function setPointerOpened(isPointerOpened) {
         const dialog = getDialog();

         if (!dialog) {
            return;
         }

         if (isPointerOpened) {
            dialog.setAttribute(OverlayModal.POINTER_OPENED_ATTRIBUTE, '');
            return;
         }

         dialog.removeAttribute(OverlayModal.POINTER_OPENED_ATTRIBUTE);
      }

      function applyTitleSemantics(dialog, title) {
         if (!title) {
            dialog.removeAttribute('aria-labelledby');
            return;
         }

         title.setAttribute('tabindex', '-1');

         if (!titleId) {
            return;
         }

         title.id = titleId;
         dialog.setAttribute('aria-labelledby', titleId);
      }

      function applyDialogSemantics() {
         const dialog = getDialog();

         if (!dialog) {
            return;
         }

         dialog.setAttribute('role', 'dialog');
         dialog.setAttribute('aria-modal', 'true');
         dialog.setAttribute('tabindex', '-1');

         const title = getTitle(dialog);

         applyTitleSemantics(dialog, title);
         decorateDialog(dialog, title);
      }

      function getFocusableElements() {
         return TooltipFocusManager.collectFocusableElements(getDialog());
      }

      function getInitialFocusTarget() {
         const dialog = getDialog();
         const title = getTitle(dialog);

         if (title) {
            return title;
         }

         const focusable = getFocusableElements();

         if (focusable.length > 0) {
            return focusable[0];
         }

         return dialog;
      }

      function containsFocus(root = getDialog()) {
         const active = getActiveElement();

         if (active && root?.contains(active)) {
            return true;
         }

         return isRelatedFocusTarget(active);
      }

      function shouldSkipBackgroundElement(element, overlayNode) {
         if (!element || element === overlayNode) {
            return true;
         }

         const tagName = String(element.tagName || '').toLowerCase();

         return OverlayModal.NON_CONTENT_TAGS.has(tagName)
            || element.hasAttribute('inert')
            || isRelatedFocusTarget(element);
      }

      function markBackgroundInert() {
         let node = getOverlay();
         const body = globalThis.document?.body ?? null;

         while (node && node !== body && node.parentElement) {
            const parent = node.parentElement;

            for (const sibling of parent.children ?? []) {
               if (shouldSkipBackgroundElement(sibling, node)) {
                  continue;
               }

               sibling.setAttribute('inert', '');
               inertedElements.push(sibling);
            }

            node = parent;
         }
      }

      function restoreBackground() {
         inertedElements.forEach((element) => {
            element.removeAttribute('inert');
         });
         inertedElements = [];
      }

      function rememberReturnFocus(returnFocusFallback) {
         const active = getActiveElement();

         if (isFocusLost(active)) {
            returnFocusEl = null;
         }
         else {
            returnFocusEl = active;
         }

         returnFocusFallbackEl = returnFocusFallback;
      }

      function activate({ returnFocusFallback = null } = {}) {
         applyDialogSemantics();

         if (isActive) {
            focusIfLost();
            return;
         }

         rememberReturnFocus(returnFocusFallback);
         isActive = true;
         setPointerOpened(lastInputWasPointer);
         moveFocus(getInitialFocusTarget());
         markBackgroundInert();
      }

      function refresh() {
         if (!isActive) {
            return;
         }

         applyDialogSemantics();
         setPointerOpened(lastInputWasPointer);
         moveFocus(getInitialFocusTarget());
      }

      function focusIfLost(preferredElement = null) {
         if (!isActive || containsFocus()) {
            return;
         }

         if (preferredElement) {
            moveFocus(preferredElement);
            return;
         }

         moveFocus(getInitialFocusTarget());
      }

      function deactivate() {
         if (!isActive) {
            return;
         }

         const shouldRestoreFocus = isFocusLost() || containsFocus(getOverlay());

         isActive = false;
         restoreBackground();
         setPointerOpened(false);

         const target = getReturnFocusTarget();
         returnFocusEl = null;
         returnFocusFallbackEl = null;

         if (target && shouldRestoreFocus) {
            moveFocus(target);
         }
      }

      function getNextFocusable(previousElement, shiftKey) {
         const focusable = getFocusableElements();
         const index = focusable.indexOf(previousElement);

         if (shiftKey) {
            return focusable[index - 1] ?? getInitialFocusTarget();
         }

         return focusable[index + 1] ?? getInitialFocusTarget();
      }

      function restoreFocusAfterTab(shiftKey, previousElement) {
         const restore = () => {
            if (!isActive || !globalThis.document) {
               return;
            }

            if (containsFocus() || isRelatedFocusTarget(getActiveElement())) {
               return;
            }

            moveFocus(getNextFocusable(previousElement, shiftKey));
         };

         if (typeof globalThis.setTimeout === 'function') {
            globalThis.setTimeout(restore, 0);
            return;
         }

         restore();
      }

      function handleTab(event) {
         if (isRelatedFocusTarget(getActiveElement())) {
            return;
         }

         const focusable = getFocusableElements();

         if (focusable.length === 0) {
            event.preventDefault();
            moveFocus(getInitialFocusTarget());
            return;
         }

         const first = focusable[0];
         const last = focusable[focusable.length - 1];
         const active = getActiveElement();
         const isOutsideList = !focusable.includes(active);

         if (event.shiftKey && (active === first || isOutsideList)) {
            event.preventDefault();
            moveFocus(last);
            return;
         }

         if (!event.shiftKey && (active === last || isOutsideList)) {
            event.preventDefault();
            moveFocus(first);
         }
      }

      function isPlainTabKey(event) {
         return event.key === 'Tab'
            && !event.altKey
            && !event.ctrlKey
            && !event.metaKey;
      }

      function handleKeydown(event) {
         // Count keys even while closed, so Enter-to-open still shows a focus ring.
         lastInputWasPointer = false;

         if (!isActive) {
            return;
         }

         setPointerOpened(false);

         if (!isPlainTabKey(event)) {
            return;
         }

         const previousElement = getActiveElement();
         handleTab(event);

         if (event.defaultPrevented) {
            return;
         }

         restoreFocusAfterTab(event.shiftKey, previousElement);
      }

      function handlePointerDown() {
         lastInputWasPointer = true;
      }

      function handleFocusIn(event) {
         if (!isActive) {
            return;
         }

         const dialog = getDialog();

         if (!dialog || dialog.contains(event.target) || isRelatedFocusTarget(event.target)) {
            return;
         }

         moveFocus(getInitialFocusTarget());
      }

      function install() {
         const doc = globalThis.document;

         doc?.addEventListener('pointerdown', handlePointerDown, true);
         doc?.addEventListener('focusin', handleFocusIn, true);
      }

      return {
         install,
         activate,
         refresh,
         deactivate,
         focusIfLost,
         handleKeydown,
         handlePointerDown,
         handleFocusIn,
         isActive: () => isActive,
      };
   }

   static getDefaultTitle() {
      return null;
   }

   static decorateNothing() {
   }
}

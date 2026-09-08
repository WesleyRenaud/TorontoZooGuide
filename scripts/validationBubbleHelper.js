export class ValidationBubbleHelper {
   static DEFAULT_CLASS_NAMES = {
      bubble: 'tzg-validation-bubble',
      icon: 'tzg-validation-bubble-icon',
      text: 'tzg-validation-bubble-text',
   };

   static VIEWPORT_PADDING = 12;
   static ANCHOR_GAP = 12;
   static ARROW_SIZE = 14;

   static resolveClassNames(classNames = {}) {
      return {
         ...ValidationBubbleHelper.DEFAULT_CLASS_NAMES,
         ...classNames,
      };
   }

   static positionValidationBubble(bubbleEl, anchorEl) {
      const anchorRect = anchorEl.getBoundingClientRect();
      const bubbleRect = bubbleEl.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      let left = anchorRect.left;
      const maxLeft = viewportWidth - bubbleRect.width - ValidationBubbleHelper.VIEWPORT_PADDING;

      if (left > maxLeft) {
         left = Math.max(ValidationBubbleHelper.VIEWPORT_PADDING, maxLeft);
      }

      let top = anchorRect.bottom + ValidationBubbleHelper.ANCHOR_GAP;
      const maxTop = viewportHeight - bubbleRect.height - ValidationBubbleHelper.VIEWPORT_PADDING;

      if (top > maxTop) {
         top = Math.max(
            ValidationBubbleHelper.VIEWPORT_PADDING,
            anchorRect.top - bubbleRect.height - ValidationBubbleHelper.ANCHOR_GAP
         );
      }

      const arrowLeft = Math.max(
         ValidationBubbleHelper.ARROW_SIZE,
         Math.min(
            bubbleRect.width - ValidationBubbleHelper.ARROW_SIZE,
            (anchorRect.left + (anchorRect.width / 2)) - left
         )
      );

      bubbleEl.style.left = `${Math.round(left)}px`;
      bubbleEl.style.top = `${Math.round(top)}px`;
      bubbleEl.style.setProperty('--tzg-validation-bubble-arrow-left', `${Math.round(arrowLeft)}px`);
   }
}

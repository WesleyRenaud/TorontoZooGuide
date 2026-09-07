export class WheelBlockerHelpers {
   static isScrollable(el) {
      if (!el) return false;
      const style = window.getComputedStyle(el);
      const overflowY = style.overflowY;
      if (overflowY !== 'auto' && overflowY !== 'scroll') return false;
      return el.scrollHeight > el.clientHeight;
   }

   static findScrollableAncestor(startEl, stopEl) {
      let el = startEl;
      while (el && el !== stopEl && el !== document.body) {
         if (WheelBlockerHelpers.isScrollable(el)) return el;
         el = el.parentElement;
      }
      return null;
   }
}

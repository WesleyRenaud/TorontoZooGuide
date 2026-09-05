function isScrollable(el) {
   if (!el) return false;
   const style = window.getComputedStyle(el);
   const overflowY = style.overflowY;
   if (overflowY !== 'auto' && overflowY !== 'scroll') return false;
   return el.scrollHeight > el.clientHeight;
}

function findScrollableAncestor(startEl, stopEl) {
   let el = startEl;
   while (el && el !== stopEl && el !== document.body) {
      if (isScrollable(el)) return el;
      el = el.parentElement;
   }
   return null;
}

export class WheelBlocker {
   static blockMapWheelWhileWizardOpen(mountEl) {
      if (!mountEl) return;

      mountEl.addEventListener(
         'wheel',
         (e) => {
            const overlay = mountEl.querySelector('.itin-overlay');
            if (!overlay) return;

            if (!overlay.contains(e.target)) return;

            const scroller = findScrollableAncestor(e.target, overlay);

            if (scroller) {
               e.stopPropagation();
               return;
            }

            e.preventDefault();
            e.stopPropagation();
         },
         { capture: true, passive: false }
      );
   }
}

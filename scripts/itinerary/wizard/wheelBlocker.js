import { WheelBlockerHelpers } from './wheelBlockerHelpers.js';
export class WheelBlocker {
   static blockMapWheelWhileWizardOpen(mountEl) {
      if (!mountEl) return;

      mountEl.addEventListener(
         'wheel',
         (e) => {
            const overlay = mountEl.querySelector('.itin-overlay');
            if (!overlay) return;

            if (!overlay.contains(e.target)) return;

            const scroller = WheelBlockerHelpers.findScrollableAncestor(e.target, overlay);

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

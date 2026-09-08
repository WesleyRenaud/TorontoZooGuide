import { WheelBlockerHelper } from './wheelBlockerHelper.js';
export class WheelBlocker {
   static blockMapWheelWhileWizardOpen(mountEl) {
      if (!mountEl) return;

      mountEl.addEventListener(
         'wheel',
         (e) => {
            const overlay = mountEl.querySelector('.itin-overlay');
            if (!overlay) return;

            if (!overlay.contains(e.target)) return;

            const scroller = WheelBlockerHelper.findScrollableAncestor(e.target, overlay);

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

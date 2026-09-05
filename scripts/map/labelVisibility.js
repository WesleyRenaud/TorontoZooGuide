export class LabelVisibility {
   static initLabelVisibilityToggle({ checkboxEl, rootEl }) {
      if (!checkboxEl || !rootEl) return;

      function sync() {
         const show = !!checkboxEl.checked;
         rootEl.classList.toggle('hide-map-labels', !show);
      }

      checkboxEl.addEventListener('change', sync);
      sync();
   }
}

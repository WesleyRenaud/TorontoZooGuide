export class RegionSelectorRendererHelpers {
   static createEmptyState(message) {
      const emptyEl = document.createElement('div');
      emptyEl.className = 'itin-empty';
      emptyEl.textContent = message;
      return emptyEl;
   }
}

export class RegionSelectorRendererHelper {
   static createEmptyState(message) {
      const emptyEl = document.createElement('div');
      emptyEl.className = 'itin-empty';
      emptyEl.textContent = message;
      return emptyEl;
   }
}

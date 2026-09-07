import { ItineraryPanelDom } from '../itineraryPanelDom.js';

export class ItineraryPanelViewsHelpers {
   static makeToggleButton({ label, view, activeView, onSelect }) {
      const button = ItineraryPanelDom.el('button', 'itin-panel-view-toggle-button', label);
      button.type = 'button';
      button.dataset.view = view;
      button.setAttribute('aria-pressed', view === activeView ? 'true' : 'false');
      button.addEventListener('click', () => onSelect(view));
      return button;
   }

   static setViewVisibility(root, selectedView) {
      root.querySelectorAll('.itin-panel-view-toggle-button').forEach((button) => {
         const isSelected = button.dataset.view === selectedView;
         button.classList.toggle('itin-panel-view-toggle-button-active', isSelected);
         button.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
      });

      root.querySelectorAll('.itin-panel-view').forEach((view) => {
         view.hidden = view.dataset.view !== selectedView;
      });
   }
}

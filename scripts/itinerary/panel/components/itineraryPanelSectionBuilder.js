import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { ItineraryPanelSectionBuilderHelper } from './itineraryPanelSectionBuilderHelper.js';
import { Strings } from '../../../strings.js';

export class ItineraryPanelSectionBuilder {
   static makeSection({
      title,
      count,
      children = [],
      stepKey,
      showEditButton = true,
   }) {
      const section = ItineraryPanelHelper.el('section', 'itin-panel-section');

      const header = ItineraryPanelHelper.el('div', 'itin-panel-section-header');

      const titleEl = ItineraryPanelHelper.el('div', 'itin-panel-section-title');
      titleEl.appendChild(document.createTextNode(title));

      const countEl = ItineraryPanelHelper.el('span', 'itin-panel-count', `(${count})`);
      titleEl.appendChild(countEl);

      const headerActions = ItineraryPanelHelper.el('div', 'itin-panel-header-actions');

      const editBtn = ItineraryPanelHelper.el('button', 'itin-panel-section-edit-btn', Strings.itinerary.actions.edit);
      editBtn.type = 'button';
      editBtn.setAttribute('aria-label', Strings.itinerary.panel.editSectionAria(title));
      editBtn.addEventListener('click', (e) => {
         e.preventDefault();
         e.stopPropagation();
         window.dispatchEvent(new CustomEvent('tzg:editItinerarySection', {
            detail: { step: stepKey || 'date' }
         }));
      });

      const toggleBtn = ItineraryPanelHelper.el('button', 'itin-panel-toggle');
      toggleBtn.type = 'button';
      toggleBtn.setAttribute('aria-label', Strings.itinerary.panel.toggleSectionAria(title));
      toggleBtn.appendChild(ItineraryPanelHelper.el('span', 'itin-panel-toggle-icon'));

      if (showEditButton) {
         headerActions.appendChild(editBtn);
      }

      headerActions.appendChild(toggleBtn);

      header.appendChild(titleEl);
      header.appendChild(headerActions);

      const body = ItineraryPanelHelper.el('div', 'itin-panel-section-body');
      const bodyInner = ItineraryPanelHelper.el('div', 'itin-panel-section-body-inner');

      children.forEach(child => bodyInner.appendChild(child));
      body.appendChild(bodyInner);

      const toggle = () => section.classList.toggle('is-collapsed');
      header.addEventListener('click', toggle);
      toggleBtn.addEventListener('click', (e) => {
         e.stopPropagation();
         toggle();
      });

      section.appendChild(header);
      section.appendChild(body);

      let resizeObserver = null;
      let applyHeightFrame = null;

      const applyHeight = () => ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight(body, bodyInner);

      function scheduleHeightUpdate() {
         cancelAnimationFrame(applyHeightFrame);
         applyHeightFrame = requestAnimationFrame(applyHeight);
      }

      requestAnimationFrame(() => {
         applyHeight();
         requestAnimationFrame(applyHeight);
      });

      bodyInner.querySelectorAll('img').forEach((image) => {
         image.addEventListener('load', scheduleHeightUpdate, { once: true });
         image.addEventListener('error', scheduleHeightUpdate, { once: true });
      });

      if (typeof ResizeObserver === 'function') {
         resizeObserver = new ResizeObserver(scheduleHeightUpdate);
         Array.from(bodyInner.children).forEach((item) => {
            resizeObserver.observe(item);
         });
      }

      const resizeHandler = () => applyHeight();
      window.addEventListener('resize', resizeHandler, { passive: true });
      section.__tzgCleanup = () => {
         cancelAnimationFrame(applyHeightFrame);
         resizeObserver?.disconnect();
         window.removeEventListener('resize', resizeHandler);
         delete section.__tzgCleanup;
      };

      return section;
   }
}

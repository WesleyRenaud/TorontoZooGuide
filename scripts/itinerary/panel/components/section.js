// scripts/itinerary/panel/components/section.js
import { el } from '../dom.js';

/**
 * Creates a collapsible itinerary panel section with:
 * - Title + count
 * - "Edit" button that jumps to the wizard step
 * - Toggle chevron
 */
export function makeSection({ title, count, children = [], stepKey }) {
   const section = el('section', 'itin-panel-section');

   const header = el('div', 'itin-panel-section-header');

   const titleEl = el('div', 'itin-panel-section-title');
   titleEl.appendChild(document.createTextNode(title));

   const countEl = el('span', 'itin-panel-count', `(${count})`);
   titleEl.appendChild(countEl);

   // Right-side actions: Edit + Toggle
   const actions = el('div', 'itin-panel-header-actions');

   const editBtn = el('button', 'itin-panel-section-edit-btn', 'Edit');
   editBtn.type = 'button';
   editBtn.setAttribute('aria-label', `Edit ${title}`);
   editBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation(); // don't toggle collapse
      window.dispatchEvent(new CustomEvent('tzg:editItinerarySection', {
         detail: { step: stepKey || 'date' }
      }));
   });

   const toggleBtn = el('button', 'itin-panel-toggle');
   toggleBtn.type = 'button';
   toggleBtn.setAttribute('aria-label', `Toggle ${title}`);
   toggleBtn.appendChild(el('span', 'itin-panel-toggle-icon'));

   actions.appendChild(editBtn);
   actions.appendChild(toggleBtn);

   header.appendChild(titleEl);
   header.appendChild(actions);

   const body = el('div', 'itin-panel-section-body');
   children.forEach(child => body.appendChild(child));

   const toggle = () => section.classList.toggle('is-collapsed');
   header.addEventListener('click', toggle);
   toggleBtn.addEventListener('click', (e) => { e.stopPropagation(); toggle(); });

   section.appendChild(header);
   section.appendChild(body);

   return section;
}
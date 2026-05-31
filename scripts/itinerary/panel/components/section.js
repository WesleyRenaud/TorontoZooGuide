import { el } from '../dom.js';

const MAX_VISIBLE_ITEMS = 3;

function updateSectionBodyHeight(body, bodyInner) {
   const items = Array.from(bodyInner.children);

   if (items.length === 0) {
      body.style.display = 'none';
      body.style.maxHeight = 'none';
      body.style.overflowY = 'hidden';
      body.style.overflowX = 'hidden';
      return;
   }

   body.style.display = '';

   if (items.length <= MAX_VISIBLE_ITEMS) {
      body.style.maxHeight = 'none';
      body.style.overflowY = 'hidden';
      body.style.overflowX = 'hidden';
      return;
   }

   const innerStyles = window.getComputedStyle(bodyInner);
   const gap = parseFloat(innerStyles.rowGap || innerStyles.gap || '0') || 0;
   const paddingTop = parseFloat(innerStyles.paddingTop || '0') || 0;
   const paddingBottom = parseFloat(innerStyles.paddingBottom || '0') || 0;

   const visibleItems = items.slice(0, MAX_VISIBLE_ITEMS);

   const itemsHeight = visibleItems.reduce((sum, item) => {
      return sum + item.getBoundingClientRect().height;
   }, 0);

   const totalGap = gap * Math.max(0, visibleItems.length - 1);
   const maxHeight = Math.ceil(itemsHeight + totalGap + paddingTop + paddingBottom);

   body.style.maxHeight = `${maxHeight}px`;
   body.style.overflowY = 'auto';
   body.style.overflowX = 'hidden';
}

export function makeSection({
   title,
   count,
   children = [],
   stepKey,
   showEditButton = true,
}) {
   const section = el('section', 'itin-panel-section');

   const header = el('div', 'itin-panel-section-header');

   const titleEl = el('div', 'itin-panel-section-title');
   titleEl.appendChild(document.createTextNode(title));

   const countEl = el('span', 'itin-panel-count', `(${count})`);
   titleEl.appendChild(countEl);

   const actions = el('div', 'itin-panel-header-actions');

   const editBtn = el('button', 'itin-panel-section-edit-btn', 'Edit');
   editBtn.type = 'button';
   editBtn.setAttribute('aria-label', `Edit ${title}`);
   editBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('tzg:editItinerarySection', {
         detail: { step: stepKey || 'date' }
      }));
   });

   const toggleBtn = el('button', 'itin-panel-toggle');
   toggleBtn.type = 'button';
   toggleBtn.setAttribute('aria-label', `Toggle ${title}`);
   toggleBtn.appendChild(el('span', 'itin-panel-toggle-icon'));

   if (showEditButton) {
      actions.appendChild(editBtn);
   }

   actions.appendChild(toggleBtn);

   header.appendChild(titleEl);
   header.appendChild(actions);

   const body = el('div', 'itin-panel-section-body');
   const bodyInner = el('div', 'itin-panel-section-body-inner');

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

   const applyHeight = () => updateSectionBodyHeight(body, bodyInner);

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

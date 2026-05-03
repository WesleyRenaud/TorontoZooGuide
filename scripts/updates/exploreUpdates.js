import { getUpdates } from '../api/mapApi.js';

function createUpdateTypeEl(update) {
   const typeEl = document.createElement('span');
   typeEl.className = `explore-update-type explore-update-type-${String(update.type || '')
      .toLowerCase()
      .replaceAll(' ', '-')}`;
   typeEl.textContent = update.type || 'Update';
   return typeEl;
}

function createUpdateCard(update, isActive = false) {
   const cardEl = document.createElement('article');
   cardEl.className = 'explore-update-card';
   cardEl.hidden = !isActive;

   const metaEl = document.createElement('div');
   metaEl.className = 'explore-update-meta';
   metaEl.appendChild(createUpdateTypeEl(update));

   const titleEl = document.createElement('h4');
   titleEl.className = 'explore-update-title';
   titleEl.textContent = update.title || 'Update';

   const descriptionEl = document.createElement('p');
   descriptionEl.className = 'explore-update-description';
   descriptionEl.textContent = update.description || '';

   cardEl.append(metaEl, titleEl, descriptionEl);
   return cardEl;
}

function getHeaderEl(listEl) {
   return listEl.closest('.explore-updates')?.querySelector('.explore-updates-header') ?? null;
}

function setSectionVisibility(listEl, isVisible) {
   const sectionEl = listEl.closest('.explore-updates');

   if (!sectionEl) {
      return;
   }

   sectionEl.hidden = !isVisible;
}

function createArrowButton({
   label,
   symbol,
   onClick,
} = {}) {
   const buttonEl = document.createElement('button');
   buttonEl.type = 'button';
   buttonEl.className = 'explore-update-arrow';
   buttonEl.textContent = symbol;
   buttonEl.setAttribute('aria-label', label);
   buttonEl.addEventListener('click', onClick);
   return buttonEl;
}

function clearNav(headerEl) {
   headerEl?.querySelector('.explore-update-nav')?.remove();
}

function renderNav({
   listEl,
   updates,
   onStep,
} = {}) {
   const headerEl = getHeaderEl(listEl);

   clearNav(headerEl);

   if (!headerEl || updates.length <= 1) {
      return;
   }

   const navEl = document.createElement('div');
   navEl.className = 'explore-update-nav';

   navEl.append(
      createArrowButton({
         label: 'Previous update',
         symbol: '<',
         onClick: () => onStep(-1),
      }),
      createArrowButton({
         label: 'Next update',
         symbol: '>',
         onClick: () => onStep(1),
      })
   );

   headerEl.appendChild(navEl);
}

function buildUpdatesPayload(dateCtx) {
   return {
      month: dateCtx.month,
      day: dateCtx.day,
   };
}

export function createExploreUpdates({
   listEl,
} = {}) {
   if (!listEl) {
      return null;
   }

   let updates = [];
   let currentIndex = 0;

   function getSafeIndex() {
      return Math.max(0, Math.min(updates.length - 1, currentIndex));
   }

   function renderCurrentUpdate() {
      if (!updates.length) {
         listEl.replaceChildren();
         setSectionVisibility(listEl, false);
         clearNav(getHeaderEl(listEl));
         return;
      }

      currentIndex = getSafeIndex();
      setSectionVisibility(listEl, true);
      listEl.replaceChildren(
         ...updates.map((update, index) => createUpdateCard(update, index === currentIndex))
      );
      renderNav({
         listEl,
         updates,
         onStep: step,
      });
   }

   function renderUpdates(nextUpdates = []) {
      updates = nextUpdates;
      currentIndex = 0;
      renderCurrentUpdate();
   }

   function step(delta) {
      if (updates.length <= 1) {
         return;
      }

      currentIndex = (currentIndex + delta + updates.length) % updates.length;
      renderCurrentUpdate();
   }

   async function refresh(dateCtx) {
      if (!dateCtx?.month || !dateCtx?.day) {
         renderUpdates([]);
         return;
      }

      try {
         renderUpdates(await getUpdates(buildUpdatesPayload(dateCtx)));
      }
      catch (err) {
         listEl.replaceChildren();
         setSectionVisibility(listEl, false);
         clearNav(getHeaderEl(listEl));
      }
   }

   renderUpdates([]);

   return { refresh };
}

export function initExploreTypeFilter({ onChange, onAnimalsUnchecked }) {
   const multiSelect = document.getElementById('typeFilter');
   if (!multiSelect) {
      return {
         getSelectedTypes: () => ['animal'],
         buildSearchIncludeFlags:
            () => ({
               includeAnimals: true,
               includePavilions: false,
               includeRestaurants: false,
               includeRestrooms: false,
               includeGiftShops: false,
               includeAttractions: false,
            }),
                  
      };
   }

   const button = multiSelect.querySelector('.multi-select-button');
   const dropdown = multiSelect.querySelector('.multi-select-dropdown');
   const checkboxes = dropdown?.querySelectorAll('input[type="checkbox"]') || [];
   const chipContainer = multiSelect.querySelector('.selected-values');

   function getSelectedTypes() {
      return Array.from(checkboxes)
         .filter(cb => cb.checked)
         .map(cb => String(cb.value || ''));
   }

   function updateSelectedText() {
      if (!chipContainer) return;
      chipContainer.innerHTML = '';

      const selectedLabels = Array.from(checkboxes)
         .filter(cb => cb.checked)
         .map(cb => cb.parentElement.textContent.trim());

      if (selectedLabels.length === 0) {
         chipContainer.innerHTML = '<span class="filter-none">None</span>';
         return;
      }

      selectedLabels.forEach(label => {
         const chip = document.createElement('span');
         chip.className = 'filter-chip';
         chip.textContent = label;
         chipContainer.appendChild(chip);
      });
   }

   button?.addEventListener('click', (e) => {
      e.stopPropagation();
      multiSelect.classList.toggle('open');
   });

   dropdown?.addEventListener('click', (e) => e.stopPropagation());

   document.addEventListener('click', () => {
      multiSelect.classList.remove('open');
   });

   checkboxes.forEach(cb => {
      cb.addEventListener('change', () => {
         updateSelectedText();

         const selected = getSelectedTypes();
         if (!selected.includes('animal')) onAnimalsUnchecked?.();

         onChange?.();
      });
   });

   updateSelectedText();

   function buildSearchIncludeFlags() {
      const selected = getSelectedTypes();
      return {
         includeAnimals: selected.includes('animal'),
         includePavilions: selected.includes('pavilion'),
         includeRestaurants: selected.includes('restaurant'),
         includeRestrooms: selected.includes('restroom'),
         includeGiftShops: selected.includes('giftShop'),
         includeAttractions: selected.includes('attraction'),
      };
   }

   return { getSelectedTypes, buildSearchIncludeFlags };
}

// small static slot used by mapPage to inject a getter into updater
initExploreTypeFilter.getSelectedTypes = () => ['animal'];
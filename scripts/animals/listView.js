import { normalizeAssetKey } from '../assets/normalizeAssetKey.js';
import { APP_STRINGS } from '../strings.js';

export function createAnimalsListView({ listEl }) {
   function clear() {
      listEl.innerHTML = '';
      listEl.scrollTop = 0;
   }

   function renderButton({ label, imageSrc, isBack = false, onClick }) {
      const btn = document.createElement('button');
      btn.classList.add('list-button');
      if (isBack) btn.classList.add('back-button');

      if (imageSrc) {
         const img = document.createElement('img');
         img.src = imageSrc;
         img.alt = label;
         img.classList.add('list-image');
         btn.appendChild(img);
      }

      btn.appendChild(document.createTextNode(label));
      btn.addEventListener('click', onClick);

      listEl.appendChild(btn);
   }

   function renderRegions(regions, { onRegionSelected }) {
      clear();

      regions.forEach(r => {
         const fileName = normalizeAssetKey(r.name);
         renderButton({
            label: r.name,
            imageSrc: `../images/details/regions/${fileName}.png`,
            onClick: () => onRegionSelected(r)
         });
      });
   }

   function renderExhibits(regionName, exhibits, { onBack, onExhibitSelected }) {
      clear();

      renderButton({
         label: APP_STRINGS.animalsPage.back,
         isBack: true,
         onClick: onBack
      });

      exhibits.forEach(exhibit => {
         const fileName = normalizeAssetKey(exhibit);
         renderButton({
            label: exhibit,
            imageSrc: `../images/details/exhibits/${fileName}.png`,
            onClick: () => onExhibitSelected(exhibit)
         });
      });
   }

   function renderAnimals(regionName, exhibitName, animals, { onBack, onAnimalSelected }) {
      clear();

      renderButton({
         label: APP_STRINGS.animalsPage.back,
         isBack: true,
         onClick: onBack
      });

      animals.forEach(animalName => {
         const normalizedExhibit = normalizeAssetKey(exhibitName);
         const normalizedAnimal = normalizeAssetKey(animalName);

         renderButton({
            label: animalName,
            imageSrc: `../images/icons/animals/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}.png`,
            onClick: () => onAnimalSelected(animalName)
         });
      });
   }

   return {
      renderRegions,
      renderExhibits,
      renderAnimals,
      clear
   };
}

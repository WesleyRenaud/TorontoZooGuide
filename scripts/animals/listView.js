import { AssetKeyNormalizer } from '../assets/assetKeyNormalizer.js';
import { Strings } from '../strings.js';

export class ListView {
   static createAnimalsListView({ listEl }) {
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
            const fileName = AssetKeyNormalizer.normalize(r.name);
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
            label: Strings.animalsPage.back,
            isBack: true,
            onClick: onBack
         });

         exhibits.forEach(exhibit => {
            const fileName = AssetKeyNormalizer.normalize(exhibit);
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
            label: Strings.animalsPage.back,
            isBack: true,
            onClick: onBack
         });

         animals.forEach(animalName => {
            const normalizedExhibit = AssetKeyNormalizer.normalize(exhibitName);
            const normalizedAnimal = AssetKeyNormalizer.normalize(animalName);

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
}

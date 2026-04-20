import { createAnimalsApi } from '../api/animalsApi.js';
import { createAnimalsListView } from './listView.js';
import { createAnimalDetailView } from './animalDetailView.js';

export function createAnimalsRouter({ listEl }) {
   const api = createAnimalsApi();
   const listView = createAnimalsListView({ listEl });
   const detailView = createAnimalDetailView({ listEl });

   async function showRegions() {
      const regions = await api.getRegions();

      listView.renderRegions(regions, {
         onRegionSelected: async (region) => {
            if (region.hasExhibits) {
               await showExhibits(region.name);
            } else {
               await showAnimals(region.name, region.name);
            }
         }
      });
   }

   async function showExhibits(regionName) {
      const exhibits = await api.getExhibitsInRegion(regionName);

      listView.renderExhibits(regionName, exhibits, {
         onBack: () => showRegions(),
         onExhibitSelected: async (exhibitName) => {
            await showAnimals(regionName, exhibitName);
         }
      });
   }

   async function showAnimals(regionName, exhibitName) {
      const animals = await api.getAnimalsInExhibit(exhibitName);

      listView.renderAnimals(regionName, exhibitName, animals, {
         onBack: () => {
            if (regionName === exhibitName) showRegions();
            else showExhibits(regionName);
         },
         onAnimalSelected: async (animalName) => {
            await showAnimalDetail(regionName, exhibitName, animalName);
         }
      });
   }

   async function showAnimalDetail(regionName, exhibitName, animalName) {
      const animalInfo = await api.getAnimalInformation(animalName);

      detailView.render(animalInfo, {
         regionName,
         exhibitName,
         onBack: () => showAnimals(regionName, exhibitName)
      });
   }

   function start() {
      showRegions();
   }

   return { start };
}

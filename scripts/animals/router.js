import { AnimalDetailView } from './animalDetailView.js';
import { AnimalsApi } from '../api/animalsApi.js';
import { ListView } from './listView.js';

export class Router {
   static createAnimalsRouter({ listEl }) {
      const listView = ListView.createAnimalsListView({ listEl });
      const detailView = AnimalDetailView.createAnimalDetailView({ listEl });
      let latestNavigationId = 0;

      function beginNavigation() {
         latestNavigationId += 1;
         return latestNavigationId;
      }

      function isLatestNavigation(navigationId) {
         return navigationId === latestNavigationId;
      }

      async function runNavigation(task, render) {
         const navigationId = beginNavigation();
         const result = await task();

         if (!isLatestNavigation(navigationId)) {
            return;
         }

         render(result);
      }

      function shouldShowExhibits(region) {
         return region?.hasExhibits === true;
      }

      function createAnimalsBackHandler(regionName, exhibitName) {
         if (regionName === exhibitName) {
            return showRegions;
         }

         return () => showExhibits(regionName);
      }

      function showRegionSelection(region) {
         if (shouldShowExhibits(region)) {
            return showExhibits(region.name);
         }

         return showAnimals(region.name, region.name);
      }

      async function showRegions() {
         await runNavigation(() => AnimalsApi.getRegions(), (regions) => {
            listView.renderRegions(regions, {
               onRegionSelected: showRegionSelection,
            });
         });
      }

      async function showExhibits(regionName) {
         await runNavigation(() => AnimalsApi.getExhibitsInRegion(regionName), (exhibits) => {
            listView.renderExhibits(regionName, exhibits, {
               onBack: showRegions,
               onExhibitSelected: exhibitName => showAnimals(regionName, exhibitName),
            });
         });
      }

      async function showAnimals(regionName, exhibitName) {
         await runNavigation(() => AnimalsApi.getAnimalsInExhibit(exhibitName), (animals) => {
            listView.renderAnimals(regionName, exhibitName, animals, {
               onBack: createAnimalsBackHandler(regionName, exhibitName),
               onAnimalSelected: animalName => showAnimalDetail(regionName, exhibitName, animalName),
            });
         });
      }

      async function showAnimalDetail(regionName, exhibitName, animalName) {
         await runNavigation(
            () => AnimalsApi.getAnimalInformation({ species: animalName, exhibit: exhibitName }),
            (animalInfo) => {
            detailView.render(animalInfo, {
               regionName,
               exhibitName,
               onBack: () => showAnimals(regionName, exhibitName),
            });
         });
      }

      function start() {
         return showRegions();
      }

      return { start };
   }
}

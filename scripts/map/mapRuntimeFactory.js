import { AttractionClosedBanner } from '../banners/attractionClosedBanner.js';
import { DrinkingFountainClosedBanner } from '../banners/drinkingFountainClosedBanner.js';
import { GiftShopClosedBanner } from '../banners/giftShopClosedBanner.js';
import { OffDisplayBanner } from '../banners/offDisplayBanner.js';
import { RestaurantClosedBanner } from '../banners/restaurantClosedBanner.js';
import { RestroomMessageBanner } from '../banners/restroomMessageBanner.js';
import { FocusController } from '../focus/focusController.js';
import { OpenGuardiansTalkLinkedAnimal } from '../guardians/openGuardiansTalkLinkedAnimal.js';
import { LabelVisibility } from './labelVisibility.js';
import { TooltipController } from '../tooltips/tooltipController.js';

export class MapRuntimeFactory {
   static hasRequiredRuntimeElements({
      mapInner,
      tooltipEl,
      viewportEl,
   } = {}) {
      return Boolean(mapInner && tooltipEl && viewportEl);
   }

   static createMapBannerSet() {
      return {
         offDisplayBanner: OffDisplayBanner.createOffDisplayBanner(),
         restaurantClosedBanner: RestaurantClosedBanner.createRestaurantClosedBanner(),
         restroomMessageBanner: RestroomMessageBanner.createRestroomMessageBanner(),
         giftShopClosedBanner: GiftShopClosedBanner.createGiftShopClosedBanner(),
         attractionClosedBanner: AttractionClosedBanner.createAttractionClosedBanner(),
         drinkingFountainClosedBanner: DrinkingFountainClosedBanner.createDrinkingFountainClosedBanner(),
      };
   }

   static createAnimalCardClickHandler(speciesOverlay) {
      return (item) => {
         const itemType = String(item?.type || '');

         if (itemType === 'animal') {
            speciesOverlay.openFromAnimal(item);
            return;
         }

         if (itemType === 'guardiansTalk') {
            void OpenGuardiansTalkLinkedAnimal.openGuardiansTalkLinkedAnimal(item);
         }
      };
   }

   static createMapTooltip({
      tooltipEl,
      speciesOverlay,
   } = {}) {
      return TooltipController.createTooltipController({
         tooltipEl,
         onAnimalCardClick: MapRuntimeFactory.createAnimalCardClickHandler(speciesOverlay),
         ...MapRuntimeFactory.createMapBannerSet(),
      });
   }

   static initMapLabels(showMapLabelsCheckbox) {
      LabelVisibility.initLabelVisibilityToggle({
         checkboxEl: showMapLabelsCheckbox,
         rootEl: document.body,
      });
   }

   static createMapFocus({
      panzoom,
      markers,
      tooltip,
      viewportEl,
   } = {}) {
      return FocusController.createFocusController({
         panzoom,
         getMarkerByCoord: (key) => markers.getMarkerByCoord(key),
         getViewportEl: () => viewportEl,
         tooltip,
         getAllMarkers: () => markers.getAllMarkers(),
      });
   }

   static createTooltipRepositioner({
      tooltip,
      hover,
   } = {}) {
      return function repositionTooltips() {
         tooltip?.reposition?.();
         hover?.reposition?.();

         requestAnimationFrame(() => {
            tooltip?.reposition?.();
            hover?.reposition?.();
         });
      };
   }
}

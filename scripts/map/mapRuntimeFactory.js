import { AttractionClosedFragment } from '../banners/attractionClosedFragment.js';
import { DrinkingFountainClosedFragment } from '../banners/drinkingFountainClosedFragment.js';
import { GiftShopClosedFragment } from '../banners/giftShopClosedFragment.js';
import { OffDisplayFragment } from '../banners/offDisplayFragment.js';
import { RestaurantClosedFragment } from '../banners/restaurantClosedFragment.js';
import { RestroomMessageFragment } from '../banners/restroomMessageFragment.js';
import { FocusController } from '../focus/focusController.js';
import { GuardiansTalkLinkedAnimalOpener } from '../guardians/guardiansTalkLinkedAnimalOpener.js';
import { LabelPresenter } from './labelPresenter.js';
import { ItemType } from '../shared/enums/itemType.js';
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
         offDisplayBanner: OffDisplayFragment.createOffDisplayBanner(),
         restaurantClosedBanner: RestaurantClosedFragment.createRestaurantClosedBanner(),
         restroomMessageBanner: RestroomMessageFragment.createRestroomMessageBanner(),
         giftShopClosedBanner: GiftShopClosedFragment.createGiftShopClosedBanner(),
         attractionClosedBanner: AttractionClosedFragment.createAttractionClosedBanner(),
         drinkingFountainClosedBanner: DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner(),
      };
   }

   static createAnimalCardClickHandler(speciesOverlay) {
      return (item) => {
         const itemType = String(item?.type || '');

         if (itemType === ItemType.ANIMAL) {
            speciesOverlay.openFromAnimal(item);
            return;
         }

         if (itemType === ItemType.GUARDIANS_TALK) {
            void GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal(item);
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
      LabelPresenter.initLabelVisibilityToggle({
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

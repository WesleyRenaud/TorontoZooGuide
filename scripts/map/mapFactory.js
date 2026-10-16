import { AppConfig } from '../config/appConfig.js';
import { MapDataSourceFactory } from './mapDataSourceFactory.js';
import { MapRuntimeFactory } from './mapRuntimeFactory.js';
import { MapStageController } from './mapStageController.js';
import { MapStore } from './mapStore.js';
import { MapUpdater } from './mapUpdater.js';
import { HoverFragment } from '../markers/hoverFragment.js';
import { MarkerController } from '../markers/markerController.js';
import { SpeciesFragment } from '../overlays/speciesFragment.js';
import { PanzoomAdapter } from './panzoomAdapter.js';

export class MapFactory {
   static createMapRuntime({
   mapInner,
   tooltipEl,
   hoverTooltipEl,
   showMapLabelsCheckbox = null,
   enableCoordinateEditing = false,
   getIncludeOffDisplay = () => false,
   getIncludeClosedRestaurants = () => false,
   getIncludeClosedRestrooms = () => false,
   getIncludeClosedGiftShops = () => false,
   getIncludeClosedAttractions = () => false,
   getTransportationRoute = () => 'none',
   getSelectedTypes = () => [],
   onDateContextChange = null,
} = {}) {
      const viewportEl = mapInner?.parentElement;

      if (!MapRuntimeFactory.hasRequiredRuntimeElements({ mapInner, tooltipEl, viewportEl })) {
         return null;
      }

      let panzoom = null;
      const markerSurface = MapStageController.mount(mapInner, (rect) => {
         MapStageController.syncPan(panzoom, rect);
      });
      const frame = MapStageController.frameFor(mapInner);
      const panzoomOptions = {
         contain: AppConfig.DEFAULT_MAP_CONTAIN,
      };

      if (frame) {
         panzoomOptions.startX = frame.left;
         panzoomOptions.startY = frame.top;
      }

      panzoom = PanzoomAdapter.createPanzoom(markerSurface, panzoomOptions);

      if (frame) {
         MapStageController.syncPan(panzoom, frame);
      }
      const store = MapStore.createMapStore();
      const sources = MapDataSourceFactory.createDataSources(store);
      const hover = HoverFragment.createHoverTooltip(hoverTooltipEl);
      const speciesOverlay = SpeciesFragment.initSpeciesOverlay();

      const tooltip = MapRuntimeFactory.createMapTooltip({
         tooltipEl,
         speciesOverlay,
      });

      MapRuntimeFactory.initMapLabels(showMapLabelsCheckbox);

      const markers = MarkerController.createMarkerLayer({
         markerSurface,
         tooltip,
         hover,
         enableCoordinateEditing,
      });

      const focus = MapRuntimeFactory.createMapFocus({
         panzoom,
         markers,
         tooltip,
         viewportEl,
      });

      const updater = MapUpdater.createMapUpdater({
         store,
         sources,
         markers,
         focus,
         getIncludeOffDisplay,
         getIncludeClosedRestaurants,
         getIncludeClosedRestrooms,
         getIncludeClosedGiftShops,
         getIncludeClosedAttractions,
         getTransportationRoute,
         getSelectedTypes,
         onDateContextChange,
      });

      return {
         panzoom,
         store,
         sources,
         hover,
         tooltip,
         markers,
         focus,
         updater,
         repositionTooltips: MapRuntimeFactory.createTooltipRepositioner({
            tooltip,
            hover,
         }),
      };
   }
}

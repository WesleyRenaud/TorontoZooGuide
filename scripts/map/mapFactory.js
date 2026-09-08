import { AppConfig } from '../config/appConfig.js';
import { MapDataSourceFactory } from './mapDataSourceFactory.js';
import { MapRuntimeFactory } from './mapRuntimeFactory.js';
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

      const panzoom = PanzoomAdapter.createPanzoom(mapInner, { contain: AppConfig.DEFAULT_MAP_CONTAIN });
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
         mapInner,
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

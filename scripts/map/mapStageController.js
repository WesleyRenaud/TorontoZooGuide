import { ZooMapConstants } from '../shared/zooMapConstants.js';

export class MapStageController {
   static STAGE_ID = 'mapStage';

   static MARKER_LAYER_ID = 'markerLayer';

   static anchoredMarkerLayers = new WeakSet();

   static COVER_SLACK_PX = 1;

   static coverRect(containerWidth, containerHeight, contentWidth, contentHeight) {
      if (!(containerWidth > 0) || !(containerHeight > 0) || !(contentWidth > 0) || !(contentHeight > 0)) {
         return null;
      }

      const contentAspect = contentWidth / contentHeight;

      if ((containerWidth / containerHeight) > contentAspect) {
         const width = containerWidth;
         const height = width / contentAspect;

         return {
            left: 0,
            top: (containerHeight - height) / 2,
            width,
            height,
         };
      }

      const height = containerHeight;
      const width = height * contentAspect;

      return {
         left: (containerWidth - width) / 2,
         top: 0,
         width,
         height,
      };
   }

   static frameFor(mapInner) {
      return MapStageController.coverRect(
         mapInner?.clientWidth,
         mapInner?.clientHeight,
         ZooMapConstants.ZOO_MAP_WIDTH_PX,
         ZooMapConstants.ZOO_MAP_HEIGHT_PX
      );
   }

   static apply(stage, mapInner) {
      const rect = MapStageController.frameFor(mapInner);

      if (!stage || !rect) {
         return null;
      }

      const stageWidth = rect.width + MapStageController.COVER_SLACK_PX;
      const stageHeight = rect.height + MapStageController.COVER_SLACK_PX;

      stage.style.left = '0px';
      stage.style.top = '0px';
      stage.style.width = `${stageWidth}px`;
      stage.style.height = `${stageHeight}px`;
      MapStageController.placeMarkerLayer(stage, mapInner, rect, stageWidth, stageHeight);
      return rect;
   }

   static placeMarkerLayer(stage, mapInner, rect, stageWidth, stageHeight) {
      const layer = stage.querySelector?.(`#${MapStageController.MARKER_LAYER_ID}`);

      if (!layer || MapStageController.anchoredMarkerLayers.has(layer)) {
         return;
      }

      MapStageController.anchoredMarkerLayers.add(layer);
      layer.style.left = `${(-rect.left / stageWidth) * 100}%`;
      layer.style.top = `${(-rect.top / stageHeight) * 100}%`;
      layer.style.width = `${(mapInner.clientWidth / stageWidth) * 100}%`;
      layer.style.height = `${(mapInner.clientHeight / stageHeight) * 100}%`;
   }

   static ensureMarkerLayer(stage) {
      const existing = stage.querySelector?.(`#${MapStageController.MARKER_LAYER_ID}`);

      if (existing) {
         return existing;
      }

      const layer = document.createElement('div');
      layer.id = MapStageController.MARKER_LAYER_ID;
      stage.appendChild(layer);
      return layer;
   }

   static syncPan(panzoom, rect) {
      if (panzoom.getScale() === 1) {
         panzoom.pan(rect.left, rect.top, { animate: false });
         return;
      }

      const pan = panzoom.getPan();
      panzoom.pan(pan.x, pan.y, { animate: false });
   }

   static findStage(mapInner) {
      return mapInner.querySelector?.(`#${MapStageController.STAGE_ID}`) ?? null;
   }

   static createStage(mapInner) {
      const stage = document.createElement('div');
      stage.id = MapStageController.STAGE_ID;
      const mount = mapInner.querySelector?.('#zooMapMount');

      if (mount) {
         stage.appendChild(mount);
      }

      MapStageController.ensureMarkerLayer(stage);

      if (typeof mapInner.prepend === 'function') {
         mapInner.prepend(stage);
      } else {
         mapInner.appendChild(stage);
      }

      return stage;
   }

   static observe(mapInner, onResize) {
      if (typeof ResizeObserver !== 'function') {
         return;
      }

      const observer = new ResizeObserver(() => {
         onResize();
      });
      observer.observe(mapInner);
   }

   static mount(mapInner, onFrame) {
      if (!mapInner) {
         return null;
      }

      const existingStage = MapStageController.findStage(mapInner);
      const stage = existingStage || MapStageController.createStage(mapInner);
      MapStageController.ensureMarkerLayer(stage);
      const publish = () => {
         const rect = MapStageController.apply(stage, mapInner);

         if (rect && onFrame) {
            onFrame(rect);
         }
      };

      MapStageController.apply(stage, mapInner);

      if (!existingStage) {
         MapStageController.observe(mapInner, publish);
      }

      return stage;
   }
}

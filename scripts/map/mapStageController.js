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

   static fit(mapInner) {
      const rect = MapStageController.frameFor(mapInner);

      if (!rect) {
         return null;
      }

      const box = mapInner.getBoundingClientRect?.();
      const containerWidth = box?.width > 0 ? box.width : mapInner.clientWidth;
      const containerHeight = box?.height > 0 ? box.height : mapInner.clientHeight;
      const fittedAxis = (overflow, coverStart, coverSize, containerSize) => {
         if (overflow > MapStageController.COVER_SLACK_PX) {
            return {
               start: coverStart,
               size: coverSize + MapStageController.COVER_SLACK_PX,
            };
         }

         return {
            start: 0,
            size: containerSize,
         };
      };
      const width = fittedAxis(rect.width - containerWidth, rect.left, rect.width, containerWidth);
      const height = fittedAxis(rect.height - containerHeight, rect.top, rect.height, containerHeight);

      return {
         left: width.start,
         top: height.start,
         width: width.size,
         height: height.size,
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
      const fit = MapStageController.fit(mapInner);

      if (!stage || !fit) {
         return null;
      }

      stage.style.left = '0px';
      stage.style.top = '0px';
      stage.style.width = `${fit.width}px`;
      stage.style.height = `${fit.height}px`;
      MapStageController.placeMarkerLayer(stage, mapInner);
      return fit;
   }

   static referenceContainerSize(mapInner) {
      const fallback = {
         width: mapInner?.clientWidth ?? 0,
         height: mapInner?.clientHeight ?? 0,
      };

      if (typeof getComputedStyle !== 'function' || !document?.documentElement || !window?.innerWidth) {
         return fallback;
      }

      const styles = getComputedStyle(document.documentElement);
      const panel = styles.getPropertyValue('--map-marker-panel-width').trim();
      const frame = styles.getPropertyValue('--map-frame-height').trim();

      if (!panel || !frame) {
         return fallback;
      }

      const probe = document.createElement('div');
      probe.style.position = 'absolute';
      probe.style.visibility = 'hidden';
      probe.style.pointerEvents = 'none';
      probe.style.width = panel;
      probe.style.height = frame;
      document.documentElement.appendChild(probe);
      const box = probe.getBoundingClientRect();
      probe.remove();

      if (!(box.width > 0) || !(box.height > 0)) {
         return fallback;
      }

      return {
         width: Math.max(0, window.innerWidth - box.width),
         height: box.height,
      };
   }

   static markerLayerFrame(containerWidth, containerHeight) {
      const rect = MapStageController.coverRect(
         containerWidth,
         containerHeight,
         ZooMapConstants.ZOO_MAP_WIDTH_PX,
         ZooMapConstants.ZOO_MAP_HEIGHT_PX
      );

      if (!rect) {
         return null;
      }

      const stageWidth = rect.width + MapStageController.COVER_SLACK_PX;
      const stageHeight = rect.height + MapStageController.COVER_SLACK_PX;

      return {
         left: (-rect.left / stageWidth) * 100,
         top: (-rect.top / stageHeight) * 100,
         width: (containerWidth / stageWidth) * 100,
         height: (containerHeight / stageHeight) * 100,
      };
   }

   static placeMarkerLayer(stage, mapInner) {
      const layer = stage.querySelector?.(`#${MapStageController.MARKER_LAYER_ID}`);

      if (!layer || MapStageController.anchoredMarkerLayers.has(layer)) {
         return;
      }

      const container = MapStageController.referenceContainerSize(mapInner);
      const frame = MapStageController.markerLayerFrame(container.width, container.height);

      if (!frame) {
         return;
      }

      MapStageController.anchoredMarkerLayers.add(layer);
      layer.style.left = `${frame.left}%`;
      layer.style.top = `${frame.top}%`;
      layer.style.width = `${frame.width}%`;
      layer.style.height = `${frame.height}%`;
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

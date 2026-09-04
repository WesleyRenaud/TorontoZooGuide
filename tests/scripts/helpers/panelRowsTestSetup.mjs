import { afterEach, beforeEach } from 'node:test';

import { ItineraryAdjustmentTypes } from '../../../scripts/itinerary/itineraryAdjustmentTypes.js';
import {
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
} from '../../../scripts/shared/constants.js';
import { installTestWindow } from './domMock.mjs';

const EMPTY_ITINERARY = {
   animals: [],
   attractions: [],
   transportations: [],
   guardiansTalks: [],
   wildEncounters: [],
};

const TEST_ITINERARY_CONFIG = {
   eventTypes: [
      'arrival',
      'breakfast',
      'break',
      'departure',
      'dinner',
      'lunch',
      'shopping',
      'snack',
   ],
   visitBoundaryEventTypes: {
      arrival: 'arrival',
      departure: 'departure',
   },
};

function createNode(tagName, className = '', textContent = '') {
   const children = [];
   const listeners = {};
   const attributes = {};
   const classes = new Set(className ? className.split(/\s+/).filter(Boolean) : []);
   let ownTextContent = textContent;

   const node = {
      tagName,
      get className() {
         return [...classes].join(' ');
      },
      set className(value) {
         classes.clear();

         for (const token of String(value).split(/\s+/)) {
            if (token) {
               classes.add(token);
            }
         }
      },
      get textContent() {
         if (children.length === 0) {
            return ownTextContent;
         }

         return children
            .map((child) => child.textContent ?? '')
            .join('');
      },
      set textContent(value) {
         ownTextContent = value;

         for (const child of children) {
            child.parentElement = null;
            child.parent = null;
         }

         children.length = 0;
      },
      children,
      listeners,
      attributes,
      hidden: false,
      disabled: false,
      style: {
         setProperty(name, value) {
            attributes[`style:${name}`] = value;
         },
      },
      classList: {
         contains(value) {
            return classes.has(value);
         },
         add(value) {
            classes.add(value);
         },
         toggle(value, shouldAdd) {
            if (shouldAdd) {
               classes.add(value);
            } else {
               classes.delete(value);
            }
         },
      },
      appendChild(child) {
         child.parentElement = node;
         child.parent = node;
         children.push(child);
         return child;
      },
      insertBefore(newChild, referenceChild) {
         newChild.parentElement = node;
         newChild.parent = node;

         if (!referenceChild) {
            children.push(newChild);
            return newChild;
         }

         const referenceIndex = children.indexOf(referenceChild);

         if (referenceIndex < 0) {
            children.push(newChild);
            return newChild;
         }

         children.splice(referenceIndex, 0, newChild);
         return newChild;
      },
      removeChild(child) {
         const childIndex = children.indexOf(child);

         if (childIndex >= 0) {
            children.splice(childIndex, 1);
         }

         child.parentElement = null;
         child.parent = null;

         return child;
      },
      closest(selector) {
         let current = node;

         while (current) {
            if (nodeMatchesSelector(current, selector)) {
               return current;
            }

            current = current.parentElement ?? current.parent;
         }

         return null;
      },
      get offsetHeight() {
         if (classes.has('itinerary-day-open-pill')) {
            return TIMELINE_POINT_PILL_HEIGHT_PX;
         }

         if (classes.has('itinerary-day-grid-line')) {
            return TIMELINE_SLOT_HEIGHT_PX;
         }

         return 0;
      },
      append(...items) {
         children.push(...items);
      },
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
      },
      contains(target) {
         if (target === node) {
            return true;
         }

         return children.some((child) => child.contains?.(target) ?? false);
      },
      click() {
         const event = {
            preventDefault() {},
            stopPropagation() {},
         };

         listeners.click?.(event);
      },
      getBoundingClientRect() {
         return {
            height: classes.has('itinerary-day-open-pill')
               ? TIMELINE_POINT_PILL_HEIGHT_PX
               : 100,
         };
      },
      setAttribute(name, value) {
         attributes[name] = value;
      },
      getAttribute(name) {
         return attributes[name] ?? null;
      },
      querySelector(selector) {
         const classNameToFind = selector.startsWith('.')
            ? selector.slice(1)
            : selector;
         const stack = [...children];

         while (stack.length > 0) {
            const child = stack.shift();

            if (child.className?.split(/\s+/).includes(classNameToFind)) {
               return child;
            }

            stack.push(...(child.children ?? []));
         }

         return null;
      },
      querySelectorAll(selector) {
         const matches = [];
         const classNameToFind = selector.startsWith('.')
            ? selector.slice(1)
            : selector;
         const stack = [...children];

         while (stack.length > 0) {
            const child = stack.shift();

            if (child.className?.split(/\s+/).includes(classNameToFind)) {
               matches.push(child);
            }

            stack.push(...(child.children ?? []));
         }

         return matches;
      },
   };

   if (className) {
      node.className = className;
   }

   return node;
}

function nodeMatchesSelector(node, selector) {
   if (!node || selector[0] !== '.') {
      return false;
   }

   const className = selector.slice(1);
   return node.classList?.contains(className) ?? false;
}

function allTextFor(node) {
   const childText = (node.children ?? [])
      .map(allTextFor)
      .filter((text) => text.length > 0);

   if (childText.length > 0) {
      return childText.join(' ');
   }

   return node.textContent ?? '';
}

function timelinePillTexts(planner) {
   const timeline = planner.querySelector('.itinerary-day-timeline');

   return [...(timeline?.querySelectorAll('.itinerary-day-open-pill') ?? [])].map(allTextFor);
}

function timelineScheduledPillTexts(planner) {
   const timeline = planner.querySelector('.itinerary-day-timeline');

   return [
      ...(timeline?.querySelectorAll('.itinerary-day-scheduled-pill') ?? []),
      ...(timeline?.querySelectorAll('.itinerary-day-event') ?? []),
   ].map(allTextFor);
}

function boundaryMarkerByLabel(planner, label) {
   return [...planner.querySelectorAll('.itinerary-day-boundary-marker')].find((marker) => (
      marker.attributes?.['aria-label'] === label
   ));
}

function boundaryMarkerStripByLabel(planner, label) {
   return boundaryMarkerByLabel(planner, label)?.parentElement ?? null;
}

function textFor(row, selector) {
   return row.querySelector(selector)?.textContent ?? '';
}

function imageSrcFor(row) {
   return row.querySelector('.itin-panel-thumb')?.children[0]?.src ?? '';
}


const documentListeners = new Map();

export function installPanelRowsTestHooks() {
   
   beforeEach(() => {
      documentListeners.clear();
      const documentBody = createNode('body');
   
      globalThis.document = {
         body: documentBody,
         createElement: (tagName) => createNode(tagName),
         createTextNode: (textContent) => createNode('#text', '', textContent),
         addEventListener(eventName, handler) {
            const handlers = documentListeners.get(eventName) ?? [];
            handlers.push(handler);
            documentListeners.set(eventName, handlers);
         },
         removeEventListener(eventName, handler) {
            const handlers = documentListeners.get(eventName) ?? [];
            documentListeners.set(
               eventName,
               handlers.filter((registeredHandler) => registeredHandler !== handler)
            );
         },
      };
      installTestWindow();
      ItineraryAdjustmentTypes.updateItineraryAdjustmentTypesFromConfig({
         adjustmentTypes: {
            ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
            DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
         },
      });
      globalThis.requestAnimationFrame = (callback) => callback();
   });
   
   afterEach(() => {
      delete globalThis.document;
      delete globalThis.requestAnimationFrame;
   });
}

export {
   EMPTY_ITINERARY,
   TEST_ITINERARY_CONFIG,
   allTextFor,
   boundaryMarkerByLabel,
   boundaryMarkerStripByLabel,
   createNode,
   documentListeners,
   imageSrcFor,
   textFor,
   timelinePillTexts,
   timelineScheduledPillTexts,
};

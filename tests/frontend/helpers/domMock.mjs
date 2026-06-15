/** Minimal DOM stubs for itinerary panel component tests. */

import {
   TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
   TIMELINE_SLOT_HEIGHT_PX,
} from '../../../scripts/shared/constants.js';
import { createDomNode } from './domNodeMock.mjs';
import { queryNodes, querySelectorInNode } from './domSelectorMock.mjs';

export { createDomNode };

export function installDocument() {
   const itineraryPanel = createDomNode('div', 'itinerary-panel');
   const itineraryFlow = createDomNode('div', 'itinerary-flow');
   itineraryFlow.id = 'itineraryFlow';
   const body = createDomNode('body');

   body.appendChild = (child) => {
      body.children.push(child);
      return child;
   };
   body.appendChild(itineraryPanel);
   body.appendChild(itineraryFlow);

   globalThis.document = {
      body,
      getElementById: (id) => {
         if (id === 'itineraryFlow') {
            return itineraryFlow;
         }

         return null;
      },
      addEventListener: () => {},
      removeEventListener: () => {},
      createElement: (tagName) => {
         if (tagName === 'button') {
            return createDomNode('button');
         }

         return createDomNode(tagName);
      },
      createDocumentFragment: () => {
         const fragment = createDomNode('#fragment');
         fragment.appendChild = (child) => {
            fragment.children.push(child);
            return child;
         };
         return fragment;
      },
      createTextNode: (textContent) => createDomNode('#text', '', textContent),
      querySelector: (selector) => (
         querySelectorInNode(body, selector)
         ?? querySelectorInNode(itineraryPanel, selector)
         ?? querySelectorInNode(itineraryFlow, selector)
      ),
      querySelectorAll: (selector) => {
         const matches = [];
         const seen = new Set();

         for (const root of [body, itineraryPanel, itineraryFlow]) {
            for (const node of queryNodes(root, selector)) {
               if (!seen.has(node)) {
                  seen.add(node);
                  matches.push(node);
               }
            }
         }

         return matches;
      },
   };
}

export function teardownDocument() {
   delete globalThis.document;
   delete globalThis.requestAnimationFrame;
}

export function installTestWindow() {
   globalThis.requestAnimationFrame = (callback) => {
      callback();
      return 0;
   };

   const getComputedStyle = (element) => ({
      gap: '0',
      paddingBottom: '0',
      paddingTop: '0',
      rowGap: '0',
      getPropertyValue(property) {
         if (
            property === '--itinerary-half-hour-slot-height'
            && element?.classList?.contains('itinerary-day-timeline')
         ) {
            return `${TIMELINE_SLOT_HEIGHT_PX}px`;
         }

         if (
            property === '--itinerary-pill-strip-top-offset'
            && element?.classList?.contains('itinerary-day-timeline')
         ) {
            return `${TIMELINE_PILL_STRIP_TOP_OFFSET_PX}px`;
         }

         return '';
      },
   });

   globalThis.getComputedStyle = getComputedStyle;

   globalThis.window = {
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => true,
      getComputedStyle,
      open: () => {},
   };
}

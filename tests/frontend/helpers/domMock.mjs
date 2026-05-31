/** Minimal DOM stubs for itinerary panel component tests. */

export function createDomNode(tagName = 'div', className = '', textContent = '') {
   const children = [];
   const listeners = {};
   const classes = new Set(className ? className.split(/\s+/).filter(Boolean) : []);
   const attributes = {};

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
      textContent,
      children,
      listeners,
      dataset: {},
      hidden: false,
      type: '',
      tabIndex: 0,
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
            }
            else {
               classes.delete(value);
            }
         },
      },
      appendChild(child) {
         children.push(child);
         return child;
      },
      append(...items) {
         children.push(...items);
      },
      replaceChildren(...items) {
         children.length = 0;

         for (const item of items) {
            if (item.tagName === '#fragment') {
               children.push(...item.children);
            }
            else {
               children.push(item);
            }
         }
      },
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
      },
      click() {
         listeners.click?.();
      },
      remove() {},
      setAttribute(name, value) {
         attributes[name] = value;
         node[name] = value;
      },
      getAttribute(name) {
         return attributes[name] ?? node[name] ?? null;
      },
      querySelector(selector) {
         return queryNode(node, selector);
      },
      querySelectorAll(selector) {
         return queryNodes(node, selector);
      },
      focus() {},
   };

   return node;
}

function queryNode(root, selector) {
   if (!selector.startsWith('.')) {
      return null;
   }

   const classNameToFind = selector.slice(1);
   const stack = [root];

   while (stack.length > 0) {
      const current = stack.shift();

      if (
         current !== root
         && current.className?.split(/\s+/).includes(classNameToFind)
      ) {
         return current;
      }

      stack.push(...current.children);
   }

   return null;
}

function queryNodes(root, selector) {
   if (!selector.startsWith('.')) {
      return [];
   }

   const classNameToFind = selector.slice(1);
   const matches = [];
   const stack = [root];

   while (stack.length > 0) {
      const current = stack.shift();

      if (
         current !== root
         && current.className?.split(/\s+/).includes(classNameToFind)
      ) {
         matches.push(current);
      }

      stack.push(...current.children);
   }

   return matches;
}

function nodeMatchesSelector(node, selector) {
   if (!node || selector[0] !== '.') {
      return false;
   }

   const className = selector.slice(1);
   return node.classList?.contains(className) ?? false;
}

function querySelectorInNode(node, selector) {
   if (!node) {
      return null;
   }

   if (nodeMatchesSelector(node, selector)) {
      return node;
   }

   for (const child of node.children ?? []) {
      const match = querySelectorInNode(child, selector);

      if (match) {
         return match;
      }
   }

   return null;
}

export function installDocument() {
   const itineraryPanel = createDomNode('div', 'itinerary-panel');
   const body = createDomNode('body');

   body.appendChild = (child) => {
      body.children.push(child);
      return child;
   };
   body.appendChild(itineraryPanel);

   globalThis.document = {
      body,
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
      ),
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

   globalThis.window = {
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => true,
      getComputedStyle: () => ({
         gap: '0',
         paddingBottom: '0',
         paddingTop: '0',
         rowGap: '0',
      }),
      open: () => {},
   };
}

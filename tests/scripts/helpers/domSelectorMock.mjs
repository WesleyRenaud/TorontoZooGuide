export function queryNode(root, selector) {
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

      stack.push(...(current.children ?? []));
   }

   return null;
}

export function queryNodes(root, selector) {
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

      stack.push(...(current.children ?? []));
   }

   return matches;
}

export function nodeMatchesSelector(node, selector) {
   if (!node || !selector) {
      return false;
   }

   if (selector[0] === '.') {
      const className = selector.slice(1);
      return node.classList?.contains(className) ?? false;
   }

   const dataAttributeMatch = selector.match(/^\[data-([^\]=]+)(?:="([^"]*)")?\]$/);

   if (dataAttributeMatch) {
      const datasetKey = dataAttributeMatch[1].replace(
         /-([a-z])/g,
         (_, character) => character.toUpperCase()
      );
      const expectedValue = dataAttributeMatch[2];
      const actualValue = node.dataset?.[datasetKey];

      if (expectedValue === undefined) {
         return actualValue != null && actualValue !== '';
      }

      return String(actualValue) === expectedValue;
   }

   return false;
}

export function querySelectorInNode(node, selector) {
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

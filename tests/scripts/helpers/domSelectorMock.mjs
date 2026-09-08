export function queryNode(root, selector) {
   if (!root || !selector) {
      return null;
   }

   for (const child of root.children ?? []) {
      const match = querySelectorInNode(child, selector);

      if (match) {
         return match;
      }
   }

   return null;
}

export function queryNodes(root, selector) {
   if (!root || !selector) {
      return [];
   }

   const matches = [];
   const stack = [...(root.children ?? [])];

   while (stack.length > 0) {
      const current = stack.shift();

      if (nodeMatchesSelector(current, selector)) {
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

   if (selector[0] === '#') {
      return node.id === selector.slice(1);
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

   const tagAttributeMatch = selector.match(
      /^([a-zA-Z][\w-]*)?(?:\[([^\=\]]+)(?:="([^"]*)")?\])?$/
   );

   if (tagAttributeMatch && (tagAttributeMatch[1] || tagAttributeMatch[2])) {
      const tagName = tagAttributeMatch[1];
      const attributeName = tagAttributeMatch[2];
      const attributeValue = tagAttributeMatch[3];

      if (tagName && String(node.tagName || '').toLowerCase() !== tagName.toLowerCase()) {
         return false;
      }

      if (!attributeName) {
         return true;
      }

      const actualValue = node.getAttribute?.(attributeName) ?? node[attributeName];

      if (attributeValue === undefined) {
         return actualValue != null && actualValue !== '';
      }

      return String(actualValue) === attributeValue;
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

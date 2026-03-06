// scripts/itinerary/panel/dom.js
export function el(tag, className, text) {
   const node = document.createElement(tag);
   if (className) node.className = className;
   if (text != null) node.textContent = text;
   return node;
}

export function safeImg(src) {
   const img = document.createElement('img');
   img.src = src;
   img.alt = '';
   img.loading = 'lazy';
   img.onerror = () => { img.style.display = 'none'; };
   return img;
}
let cachedSpecies = null;
let cachedExhibits = null;
let cachedRestaurants = null;
let cachedGiftShops = null;
let cachedAttractions = null;

export async function postJson(url, data) {
   const response = await fetch(url, {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
   });

   return await response.json();
}

export function setStatus(el, message, kind = '') {
   if(!el) return;

   el.textContent = message || '';
   el.classList.remove('is-success', 'is-error');

   if(kind) {
      el.classList.add(kind);
   }
}

export function populateExhibitDropdown(selectEl, exhibits) {
   if(!selectEl) return;

   selectEl.innerHTML = '';

   const placeholder = document.createElement('option');
   placeholder.value = '';
   placeholder.textContent = 'Select an exhibit';
   selectEl.appendChild(placeholder);

   exhibits
      .slice()
      .sort((a, b) => {
         const aName =
            typeof a === 'string'
               ? a
               : String(a.name ?? a.NAME ?? '');

         const bName =
            typeof b === 'string'
               ? b
               : String(b.name ?? b.NAME ?? '');

         return aName.localeCompare(bName);
      })
      .forEach(exhibit => {
         const name =
            typeof exhibit === 'string'
               ? exhibit
               : exhibit.name ?? exhibit.NAME ?? '';

         if(!name) return;

         const option = document.createElement('option');
         option.value = name;
         option.textContent = name;
         selectEl.appendChild(option);
      });
}

export function populateRestaurantDropdown(selectEl, restaurants) {
   if(!selectEl) return;

   selectEl.innerHTML = '';

   const placeholder = document.createElement('option');
   placeholder.value = '';
   placeholder.textContent = 'Select a restaurant';
   selectEl.appendChild(placeholder);

   restaurants
      .slice()
      .sort((a, b) => {
         const aName =
            typeof a === 'string'
               ? a
               : String(a.name ?? a.NAME ?? '');

         const bName =
            typeof b === 'string'
               ? b
               : String(b.name ?? b.NAME ?? '');

         return aName.localeCompare(bName);
      })
      .forEach(restaurant => {
         const name =
            typeof restaurant === 'string'
               ? restaurant
               : restaurant.name ?? restaurant.NAME ?? '';

         if(!name) return;

         const option = document.createElement('option');
         option.value = name;
         option.textContent = name;
         selectEl.appendChild(option);
      });
}

export function populateGiftShopDropdown(selectEl, giftShops) {
   if(!selectEl) return;

   selectEl.innerHTML = '';

   const placeholder = document.createElement('option');
   placeholder.value = '';
   placeholder.textContent = 'Select a gift shop';
   selectEl.appendChild(placeholder);

   giftShops
      .slice()
      .sort((a, b) => {
         const aName =
            typeof a === 'string'
               ? a
               : String(a.name ?? a.NAME ?? '');

         const bName =
            typeof b === 'string'
               ? b
               : String(b.name ?? b.NAME ?? '');

         return aName.localeCompare(bName);
      })
      .forEach(giftShop => {
         const name =
            typeof giftShop === 'string'
               ? giftShop
               : giftShop.name ?? giftShop.NAME ?? '';

         if(!name) return;

         const option = document.createElement('option');
         option.value = name;
         option.textContent = name;
         selectEl.appendChild(option);
      });
}

export function populateAttractionDropdown(selectEl, attractions) {
   if(!selectEl) return;

   selectEl.innerHTML = '';

   const placeholder = document.createElement('option');
   placeholder.value = '';
   placeholder.textContent = 'Select an attraction';
   selectEl.appendChild(placeholder);

   attractions
      .slice()
      .sort((a, b) => {
         const aName =
            typeof a === 'string'
               ? a
               : String(a.name ?? a.NAME ?? '');

         const bName =
            typeof b === 'string'
               ? b
               : String(b.name ?? b.NAME ?? '');

         return aName.localeCompare(bName);
      })
      .forEach(attraction => {
         const name =
            typeof attraction === 'string'
               ? attraction
               : attraction.name ?? attraction.NAME ?? '';

         if(!name) return;

         const option = document.createElement('option');
         option.value = name;
         option.textContent = name;
         selectEl.appendChild(option);
      });
}

export async function loadSpecies() {

   if(cachedSpecies) {
      return cachedSpecies;
   }

   const result = await postJson('/get-species', {});

   const species = result?.species ?? [];

   cachedSpecies = species
      .slice()
      .sort((a, b) => a.localeCompare(b));

   return cachedSpecies;
}

export async function loadExhibits() {
   if(cachedExhibits) {
      return cachedExhibits;
   }

   const result = await postJson('/get-exhibits', {});
   const exhibits = result?.exhibits ?? [];

   cachedExhibits = exhibits
      .slice()
      .sort((a, b) => {
         const aName =
            typeof a === 'string'
               ? a
               : String(a.name ?? a.NAME ?? '');

         const bName =
            typeof b === 'string'
               ? b
               : String(b.name ?? b.NAME ?? '');

         return aName.localeCompare(bName);
      });

   return cachedExhibits;
}

export async function loadRestaurants() {
   if(cachedRestaurants) {
      return cachedRestaurants;
   }

   const result = await postJson('/get-restaurant-names', {});
   const restaurants = result?.restaurants ?? [];

   cachedRestaurants = restaurants
      .slice()
      .sort((a, b) => {
         const aName =
            typeof a === 'string'
               ? a
               : String(a.name ?? a.NAME ?? '');

         const bName =
            typeof b === 'string'
               ? b
               : String(b.name ?? b.NAME ?? '');

         return aName.localeCompare(bName);
      });

   return cachedRestaurants;
}

export async function loadGiftShops() {
   if(cachedGiftShops) {
      return cachedGiftShops;
   }

   const result = await postJson('/get-gift-shop-names', {});
   const giftShops = result?.gift_shops ?? [];

   cachedGiftShops = giftShops
      .slice()
      .sort((a, b) => {
         const aName =
            typeof a === 'string'
               ? a
               : String(a.name ?? a.NAME ?? '');

         const bName =
            typeof b === 'string'
               ? b
               : String(b.name ?? b.NAME ?? '');

         return aName.localeCompare(bName);
      });

   return cachedGiftShops;
}

export async function loadAttractions() {
   if(cachedAttractions) {
      return cachedAttractions;
   }

   const result = await postJson('/get-attraction-names', {});
   const attractions = result?.attractions ?? [];

   cachedAttractions = attractions
      .slice()
      .sort((a, b) => {
         const aName =
            typeof a === 'string'
               ? a
               : String(a.name ?? a.NAME ?? '');

         const bName =
            typeof b === 'string'
               ? b
               : String(b.name ?? b.NAME ?? '');

         return aName.localeCompare(bName);
      });

   return cachedAttractions;
}
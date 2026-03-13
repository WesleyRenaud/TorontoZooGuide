let cachedSpecies = null;
let cachedExhibits = null;
let cachedAttractions = null;

export async function postJson( url, data ) {
   const response = await fetch( url, {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify( data )
   } );

   return await response.json();
}

export function setStatus( el, message, kind = '' ) {
   if ( !el ) return;

   el.textContent = message || '';
   el.classList.remove( 'is-success', 'is-error' );

   if ( kind ) {
      el.classList.add( kind );
   }
}

export function populateExhibitDropdown( selectEl, exhibits ) {
   if ( !selectEl ) return;

   selectEl.innerHTML = '';

   const placeholder = document.createElement( 'option' );
   placeholder.value = '';
   placeholder.textContent = 'Select an exhibit';
   selectEl.appendChild( placeholder );

   exhibits
      .slice()
      .sort( ( a, b ) => {
         const aName =
            typeof a === 'string'
               ? a
               : String( a.name ?? a.NAME ?? '' );

         const bName =
            typeof b === 'string'
               ? b
               : String( b.name ?? b.NAME ?? '' );

         return aName.localeCompare( bName );
      } )
      .forEach( exhibit => {
         const name =
            typeof exhibit === 'string'
               ? exhibit
               : exhibit.name ?? exhibit.NAME ?? '';

         if ( !name ) return;

         const option = document.createElement( 'option' );
         option.value = name;
         option.textContent = name;
         selectEl.appendChild( option );
      } );
}

export function populateAttractionDropdown( selectEl, attractions ) {
   if ( !selectEl ) return;

   selectEl.innerHTML = '';

   const placeholder = document.createElement( 'option' );
   placeholder.value = '';
   placeholder.textContent = 'Select an attraction';
   selectEl.appendChild( placeholder );

   attractions
      .slice()
      .sort( ( a, b ) => {
         const aName =
            typeof a === 'string'
               ? a
               : String( a.name ?? a.NAME ?? '' );

         const bName =
            typeof b === 'string'
               ? b
               : String( b.name ?? b.NAME ?? '' );

         return aName.localeCompare( bName );
      } )
      .forEach( attraction => {
         const name =
            typeof attraction === 'string'
               ? attraction
               : attraction.name ?? attraction.NAME ?? '';

         if ( !name ) return;

         const option = document.createElement( 'option' );
         option.value = name;
         option.textContent = name;
         selectEl.appendChild( option );
      } );
}

export async function loadSpecies() {

   if ( cachedSpecies ) {
      return cachedSpecies;
   }

   const result = await postJson( '/get-species', {} );

   const species = result?.species ?? [];

   cachedSpecies = species
      .slice()
      .sort( ( a, b ) => a.localeCompare( b ) );

   return cachedSpecies;
}

export async function loadExhibits() {
   if ( cachedExhibits ) {
      return cachedExhibits;
   }

   const result = await postJson( '/get-exhibits', {} );
   const exhibits = result?.exhibits ?? [];

   cachedExhibits = exhibits
      .slice()
      .sort( ( a, b ) => {
         const aName =
            typeof a === 'string'
               ? a
               : String( a.name ?? a.NAME ?? '' );

         const bName =
            typeof b === 'string'
               ? b
               : String( b.name ?? b.NAME ?? '' );

         return aName.localeCompare( bName );
      } );

   return cachedExhibits;
}

export async function loadAttractions() {
   if ( cachedAttractions ) {
      return cachedAttractions;
   }

   const result = await postJson( '/get-attraction-names', {} );
   const attractions = result?.attractions ?? [];

   cachedAttractions = attractions
      .slice()
      .sort( ( a, b ) => {
         const aName =
            typeof a === 'string'
               ? a
               : String( a.name ?? a.NAME ?? '' );

         const bName =
            typeof b === 'string'
               ? b
               : String( b.name ?? b.NAME ?? '' );

         return aName.localeCompare( bName );
      } );

   return cachedAttractions;
}
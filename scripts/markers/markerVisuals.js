import { likelihoodToColor, getAnimalIconUrl } from '../utils/icons.js';
import { normalizeParameter } from '../utils/normalize.js';

function resetMarkerVisual( markerEl ) {
   markerEl.textContent = '';
   markerEl.style.backgroundImage = 'none';
   markerEl.style.backgroundColor = 'transparent';
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';

   markerEl.classList.remove( 'marker-has-limited-viewing' );
}

function applyGenericIcon( markerEl, iconUrl, count ) {
   if ( count > 1 ) {
      markerEl.style.backgroundColor = 'rgba(94,150,0,0.95)';
      markerEl.style.backgroundImage = 'none';
      markerEl.textContent = String( count );
      return;
   }

   markerEl.style.backgroundColor = 'transparent';
   markerEl.style.backgroundImage = `url("${iconUrl}")`;
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';
   markerEl.textContent = '';
}

function shouldShowLimitedViewingIndicator( animal ) {
   return Boolean(
      !animal?.off_display_message
      && (
         ( animal?.has_limited_viewing_schedule && animal?.limited_viewing_message )
         || ( animal?.has_viewing_alert && animal?.viewing_alert_message )
      )
   );
}

export function applyMarkerVisual( markerEl, itemsAtPoint ) {
   if ( !markerEl ) return;

   resetMarkerVisual( markerEl );

   const items = Array.isArray( itemsAtPoint ) ? itemsAtPoint : [];
   if ( items.length === 0 ) return;

   const type = String( items[0]?.type || '' );
   const count = items.length;

   if ( type === 'animal' ) {
      const a = items[0];

      const colour = likelihoodToColor( a.likelihood );
      const colourForUrl = String( colour || '' ).replace( '#', '' );

      if ( count === 1 ) {
         markerEl.style.backgroundColor = colour;
         markerEl.style.backgroundImage = getAnimalIconUrl(
            a.exhibit,
            a.species,
            colourForUrl
         );
         markerEl.style.backgroundSize = 'cover';
         markerEl.textContent = '';
      } else {
         markerEl.style.backgroundImage = 'none';
         markerEl.style.backgroundColor = colour;
         markerEl.textContent = String( count );
      }

      if ( shouldShowLimitedViewingIndicator( a ) ) {
         markerEl.classList.add( 'marker-has-limited-viewing' );
      }

      return;
   }

   if ( type === 'pavilion' ) {
      applyGenericIcon( markerEl, '/images/generic-icons/pavilion.png', count );
      return;
   }

   if ( type === 'restaurant' ) {
      markerEl.classList.add( 'marker-restaurant' );

      const restaurant = items[0];
      const state = restaurant.is_closed ? 'closed' : 'open';
      const iconPath = `/images/generic-icons/restaurant-${state}.png`;

      applyGenericIcon( markerEl, iconPath, count );
      return;
   }

   if ( type === 'restroom' ) {
      markerEl.classList.add( 'marker-restroom' );
      applyGenericIcon( markerEl, '/images/generic-icons/restroom.png', count );
      return;
   }

   if ( type === 'giftShop' ) {
      markerEl.classList.add( 'marker-gift-shop' );

      const giftShop = items[0];
      const state = giftShop.is_closed ? 'closed' : 'open';
      const iconPath = `/images/generic-icons/gift-shop-${state}.png`;

      applyGenericIcon( markerEl, iconPath, count );
      return;
   }

   if ( type === 'attraction' ) {
      markerEl.classList.add( 'marker-attraction' );

      const attraction = items[0];
      const slug = normalizeParameter( attraction.name );

      const state = attraction.is_closed ? 'closed' : 'open';
      const iconPath = `/images/attraction-icons/${slug}-${state}.png`;

      applyGenericIcon( markerEl, iconPath, count );
      return;
   }

   if ( type === 'zoomobileStation' ) {
      markerEl.classList.add( 'marker-zoomobile-station' );
      applyGenericIcon( markerEl, '/images/generic-icons/zoomobile-station.png', count );
      return;
   }

   if ( type === 'zoomobileRouteMarker' ) {
      const routeType = items[0].route_type;

      if ( routeType == 'winter' ) {
         markerEl.style.backgroundColor = '#003366';
      } else {
         markerEl.style.backgroundColor = '#556B2F';
      }

      markerEl.classList.add( 'marker-zoomobile-route-marker' );
      return;
   }

   if ( type === 'meetTheGuardiansTalk' ) {
      markerEl.classList.add( 'marker-meet-the-guardians-talk' );
      applyGenericIcon( markerEl, '/images/generic-icons/meet-the-guardians-talk.png', count );
      return;
   }

   if ( type === 'wildEncounterMeetingSpot' || type === 'wildEncounter' ) {
      markerEl.classList.add( 'marker-wild-encounter-meeting-spot' );
      applyGenericIcon( markerEl, '/images/generic-icons/wild-encounter-meeting-spot.png', count );
      return;
   }

   markerEl.style.backgroundColor = 'rgba(94,150,0,0.95)';
   markerEl.textContent = String( count );
}

export function setMarkerToAnimalIcon( markerEl, animal ) {
   if ( !markerEl || !animal ) return;

   resetMarkerVisual( markerEl );

   const colour = likelihoodToColor( animal.likelihood );
   const colourForUrl = String( colour || '' ).replace( '#', '' );

   markerEl.style.backgroundColor = colour;
   markerEl.style.backgroundImage = getAnimalIconUrl(
      animal.exhibit,
      animal.species,
      colourForUrl
   );
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';
   markerEl.textContent = '';

   if ( shouldShowLimitedViewingIndicator( animal ) ) {
      markerEl.classList.add( 'marker-has-limited-viewing' );
   }
}
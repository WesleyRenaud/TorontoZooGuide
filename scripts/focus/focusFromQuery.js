export function initFocusFromQuery({ onFocus }) {
   const focus = new URLSearchParams(window.location.search).get('focus');
   if (!focus) return;

   const species = decodeURIComponent(focus);
   const exParam = new URLSearchParams(window.location.search).get('exhibit');
   const exhibit = exParam ? decodeURIComponent(exParam) : null;

   onFocus({ species, exhibit });

   history.replaceState({}, '', 'map.html');
}
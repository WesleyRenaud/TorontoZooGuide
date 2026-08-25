import { APP_STRINGS } from '../strings.js';

const ZOO_MAP_SVG_URL = '../images/map/zoo-map.svg';

let cachedSvgTextPromise = null;

function getZooMapMount() {
   return document.getElementById('zooMapMount');
}

function getMountedSvg(mount) {
   return mount?.querySelector('svg') ?? null;
}

function configureInlineSvg(svg) {
   svg.setAttribute('width', '100%');
   svg.setAttribute('height', '100%');
   svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');

   return svg;
}

async function fetchZooMapSvgText() {
   if (!cachedSvgTextPromise) {
      cachedSvgTextPromise = fetch(ZOO_MAP_SVG_URL)
         .then((response) => {
            if (!response.ok) {
               throw new Error(APP_STRINGS.map.loadSvgFailed(response.status));
            }

            return response.text();
         })
         .catch((error) => {
            cachedSvgTextPromise = null;
            throw error;
         });
   }

   return await cachedSvgTextPromise;
}

async function mountInlineSvg(mount) {
   mount.innerHTML = await fetchZooMapSvgText();
   return getMountedSvg(mount);
}

export async function loadInlineZooMap() {
   const mount = getZooMapMount();

   if (!mount) {
      return null;
   }

   const existingSvg = getMountedSvg(mount);

   if (existingSvg) {
      return configureInlineSvg(existingSvg);
   }

   const svg = await mountInlineSvg(mount);

   if (!svg) {
      return null;
   }

   return configureInlineSvg(svg);
}

import { Strings } from '../strings.js';

const ZOO_MAP_SVG_URL = '../images/map/zoo-map.svg';

let cachedSvgTextPromise = null;

export class InlineZooMapLoader {
   static getZooMapMount() {
      return document.getElementById('zooMapMount');
   }

   static getMountedSvg(mount) {
      return mount?.querySelector('svg') ?? null;
   }

   static configureInlineSvg(svg) {
      svg.setAttribute('width', '100%');
      svg.setAttribute('height', '100%');
      svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');

      return svg;
   }

   static async fetchZooMapSvgText() {
      if (!cachedSvgTextPromise) {
         cachedSvgTextPromise = fetch(ZOO_MAP_SVG_URL)
            .then((response) => {
               if (!response.ok) {
                  throw new Error(Strings.map.loadSvgFailed(response.status));
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

   static async mountInlineSvg(mount) {
      mount.innerHTML = await InlineZooMapLoader.fetchZooMapSvgText();
      return InlineZooMapLoader.getMountedSvg(mount);
   }
}

export async function loadInlineZooMap() {
   const mount = document.getElementById('zooMapMount');
   if (!mount) return null;

   const response = await fetch('../images/map/zoo-map.svg');
   const svgText = await response.text();

   mount.innerHTML = svgText;

   const svg = mount.querySelector('svg');
   if (!svg) return null;

   svg.setAttribute('width', '100%');
   svg.setAttribute('height', '100%');
   svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');

   return svg;
}

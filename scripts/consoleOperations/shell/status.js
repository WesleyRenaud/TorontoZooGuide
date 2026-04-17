export function setStatus(el, message, kind = '') {
   if (!el) return;

   el.textContent = message || '';
   el.classList.remove('is-success', 'is-error');

   if (kind) {
      el.classList.add(kind);
   }
}

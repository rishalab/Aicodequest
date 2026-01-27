export function msToMinSec(ms) {
    if (!ms || ms === 0) return "0 min 0 sec";
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes} min ${seconds} sec`;
}

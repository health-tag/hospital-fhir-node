import { useEffect, useState } from "react";

export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState<boolean>(window.matchMedia(query).matches);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }
    const listener = () => {
      setMatches(media.matches);
    };
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, [matches, query]);

  return matches;
}

export const useIsScreenSm = () => useMediaQuery("(min-width: 640px)");
export const useIsScreenMd = () => useMediaQuery("(min-width: 768px)");
export const useIsScreenLg = () => useMediaQuery("(min-width: 1024px)");
export const useIsScreenXl = () => useMediaQuery("(min-width: 1280px)");
export const useIsScreen2Xl = () => useMediaQuery("(min-width: 1536px)");

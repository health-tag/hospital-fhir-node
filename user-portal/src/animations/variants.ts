const dialogAnimationY = 8;
export const dialogAnimationVariants = {
  initial: {
    y: dialogAnimationY,
    opacity: 0,
  },
  animate: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.6,
    },
  },
  exit: {
    y: dialogAnimationY,
    opacity: 0,
    transition: {
      duration: 0.3,
    },
  },
};
const loginAnimationTranslation = 30;
export const loginAnimationVariants = {
  initial: (isScreenLg) =>
    isScreenLg
      ? {
          x: loginAnimationTranslation,
          opacity: 0,
        }
      : {
          y: loginAnimationTranslation,
          opacity: 0,
        },
  animate: (isScreenLg) =>
    isScreenLg
      ? {
          x: 0,
          opacity: 1,
          transition: {
            duration: 0.6,
          },
        }
      : {
          y: 0,
          opacity: 1,
          transition: {
            duration: 0.6,
          },
        },
  exit: (isScreenLg) =>
    isScreenLg
      ? {
          x: loginAnimationTranslation,
          opacity: 0,
          transition: {
            duration: 0.3,
          },
        }
      : {
          y: loginAnimationTranslation,
          opacity: 0,
          transition: {
            duration: 0.3,
          },
        },
};
const dropDownMenuAnimationY = -8;
export const dropDownMenuAnimationVariant = {
  initial: {
    y: dropDownMenuAnimationY,
    opacity: 0,
  },
  animate: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.3,
    },
  },
  exit: {
    y: dropDownMenuAnimationY,
    opacity: 0,
    transition: {
      duration: 0.15,
    },
  },
};

export const pageAnimationVariants = {
  initial: {
    y: dialogAnimationY,
    opacity: 0,
  },
  animate: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.3,
    },
  },
  exit: {
    y: dialogAnimationY,
    opacity: 0,
    transition: {
      duration: 0.15,
    },
  },
};

export const menuHeaderAnimationVariants = {
  open: {
    height: `auto`,
    opacity: 1,
    margin: `0.75rem 0.75rem 0.75rem 1.25rem`,
  },
  close: { height: `0em`, opacity: 0, margin: `0rem 0rem 0rem 1.25rem` },
};

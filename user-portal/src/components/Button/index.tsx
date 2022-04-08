type Props = {
  text: string;
  isLoading?: boolean;
  extraClass?: string;
  onClick: Function;
}

const Button = (props: Props) => {
  const {
    text,
    isLoading,
    extraClass,
    onClick
  } = props;

  return (
    <button
      className={`w-full bg-cyan-400 rounded p-2 text-black ${extraClass && extraClass}`}
      onClick={() => onClick()}
    >
      {isLoading ? 'Loading...' : text}
    </button>
  );
}
export default Button;

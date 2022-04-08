type Props = {
  type?: string;
  placeholder: string;
  value: string;
  extraClass?: string;
  setValue: Function;
}

const Input = (props: Props) => {
  const { type, placeholder, value, extraClass, setValue } = props;

  return (
    <input
      className={`w-full p-2 border rounded ${extraClass && extraClass}`}
      type={type ? type : 'text'}
      placeholder={placeholder}
      value={value}
      onChange={e => setValue(e.target.value)}
    />
  );
}
export default Input;

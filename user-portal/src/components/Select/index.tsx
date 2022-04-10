const Input = ({
  id = Math.random()
    .toString(36)
    .replace(/[^a-z]+/g, "")
    .substring(0, 6),
  label = "",
  type,
  placeholder,
  value,
  className = "",
  setValue,
  children,
  ...otherProps
}: {
  id?: string;
  label?: string;
  type?: string;
  placeholder?: string;
  value: string;
  className?: string;
  setValue: Function;
  children: React.ReactNode;
  [x: string]: any;
}) => {
  return (
    <div>
      <label htmlFor={id} className="block pb-1">
        {label}
      </label>
      <select
        id={id}
        className={`w-full p-2 rounded ${className}`}
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        {...otherProps}
      >
          {children}
      </select>
    </div>
  );
};
export default Input;

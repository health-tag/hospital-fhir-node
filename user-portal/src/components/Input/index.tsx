import { ChangeEvent, useState } from "react";

const Input = ({
  id = Math.random()
    .toString(36)
    .replace(/[^a-z]+/g, "")
    .substring(0, 6),
  label = "",
  name = "",
  type,
  placeholder,
  required = false,
  value,
  className = "",
  inputClassName = "",
  setValue,
  validator,
  ...otherProps
}: {
  id?: string;
  name?: string;
  label?: string;
  type?: string;
  required?: boolean;
  invalid?: boolean;
  invalidText?: string;
  placeholder?: string;
  value: string;
  className?: string;
  inputClassName?: string;
  setValue: Function;
  validator?: (value: string) => {
    result: boolean;
    validationMessage?: string;
  };
  [x: string]: any;
}) => {
  const [firstTimeRender, setFirstTimeRender] = useState<boolean>(true);
  const [isInvalid, setIsInvalid] = useState<boolean>(false);
  const [validationMessage, setValidationMessage] = useState<string>("");

  const onChangeHandler = (event: ChangeEvent<HTMLInputElement>) => {
    setFirstTimeRender(false);
    setValue(event.target.value);
    validatorHandler(event.target.value);
  };

  const validatorHandler = (value: string) => {
    if (validator !== undefined) {
      const { result, validationMessage } = validator(value);
      setIsInvalid(!result);
      setValidationMessage(validationMessage ?? "");
    }
  };

  return (
    <div className={className}>
      <label htmlFor={id} className="block pb-1">
        {label}
      </label>
      <input
        id={id}
        name={name}
        className={`w-full p-2 rounded ${inputClassName} ${
          isInvalid ? "required" : ""
        } ${required && !firstTimeRender && value === "" ? "required" : ""}`}
        type={type ? type : "text"}
        placeholder={placeholder}
        value={value}
        onChange={onChangeHandler}
        {...otherProps}
      />
      <div className="text-sm pt-1">
        {" "}
        {required && !firstTimeRender && value === "" && (
          <span className="text-red-400">*จำเป็นต้องใส่</span>
        )}{" "}
        {isInvalid && <span className="text-red-400">{validationMessage}</span>}
      </div>
    </div>
  );
};
export default Input;
